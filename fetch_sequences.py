#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET
import asyncio
import aiohttp
from itertools import chain
import traceback
import os
from datetime import datetime

EPOST_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/epost.fcgi"
EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
MAX_RETRY = 20
MAX_CONCURRENT_REQUESTS = 20
POST_SIZE = 50000
GET_SIZE = 10000
REQ_TIMEOUT = 1800


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:(i+n)]


class RerunableTask():
    def __init__(self, task_rerun = None):
        self.run_cnt = 0
        self.next_tasks = list()
        self.following_tasks = list()
        self.spawned_tasks = list()
        self.exception = None
        self.task_rerun = task_rerun if task_rerun != None else self


    def clear(self):
        self.next_tasks = list()
        self.spawned_tasks = list()
        self.exception = None


    async def execute(self):
        self.run_cnt += 1
        self.clear()
        if self.run_cnt > MAX_RETRY:
            raise Exception("max retry limit exceeded")

        try:
            await self.run()
        except Exception as e:
            self.exception = e

        return self


class PostIdsTaks(RerunableTask):
    def __init__(self, ids, session):
        RerunableTask.__init__(self, None)
        self.ids = ids
        self.session = session

    async def run(self):
        async with self.session.post(EPOST_URL, params = {"db": "protein"}, data = {"id": ",".join(self.ids)}) as response:
            xml = await response.text()
            tree = ET.fromstring(xml)
            web_env = tree.find("WebEnv").text
            query_key = tree.find("QueryKey").text
            
            for i in range(0, len(self.ids), GET_SIZE):
                self.next_tasks.append(RequestSequenceTask(self.session, web_env, query_key, i, GET_SIZE))


class RequestSequenceTask(RerunableTask):
    def __init__(self, session, web_env, query_key, ret_start, ret_max):
        RerunableTask.__init__(self, None)
        self.session = session
        self.web_env = web_env
        self.query_key = query_key
        self.ret_start = ret_start
        self.ret_max = ret_max
        
    async def run(self):
        response = await self.session.get(EFETCH_URL, params = {"db": "protein", "showgi": "true", "rettype": "fasta", "webenv": self.web_env, "query_key": self.query_key, "retstart": self.ret_start, "retmax": self.ret_max})
        if not response.ok:
            print("----- FAILED RESPONSE ------", file = sys.stderr)
            print(await response.text(), file = sys.stderr)
            response.close()
            raise Exception("invalid response code")

        self.spawned_tasks.append(asyncio.create_task(DownloadSequenceTask(response, self).execute()))


class DownloadSequenceTask(RerunableTask):
    def __init__(self, response, task_rerun):
        RerunableTask.__init__(self, task_rerun)
        self.response = response

    async def run(self):
        async with self.response:
            body = await self.response.text()
            print(body)


open_tasks = list()
running_tasks = set()
def on_done(f):
    try:
        t = f.result()
        if t.exception != None:
            print("----- NEW EXCEPTION ------", file = sys.stderr)
            print(datetime.now(), file = sys.stderr)
            for k, v in vars(t).items():
                print(f"{k}: {str(v)[0:250]}", file = sys.stderr)
                
            traceback.print_exception(type(t.exception), t.exception, t.exception.__traceback__)
            open_tasks.insert(0, t.task_rerun)
        else:
            running_tasks.update(t.spawned_tasks)
            list(map(lambda _: _.add_done_callback(on_done), t.spawned_tasks))
            open_tasks.extend(t.next_tasks)
            open_tasks.extend(t.following_tasks)

        running_tasks.remove(f)
    except Exception as e:
        print("FATAL - unexpected error has occured", file = sys.stderr)
        traceback.print_exception(type(e), e, e.__traceback__)
        os._exit(1) #just terminate don't perform any cleanup


async def download_sequences(ids):
    async with aiohttp.ClientSession(timeout = aiohttp.ClientTimeout(total = REQ_TIMEOUT)) as session:
        prev_task = None
        for i, c in enumerate(chunks(ids, POST_SIZE)):
            cur_task =  PostIdsTaks(c, session)
            if i == 0:
                open_tasks.append(cur_task)
            else:
                prev_task.following_tasks.append(cur_task)

            prev_task = cur_task

        while len(open_tasks) > 0 or len(running_tasks) > 0:
            if len(open_tasks) > 0 and len(running_tasks) < MAX_CONCURRENT_REQUESTS:
                td = open_tasks.pop(0)
                if td.run_cnt > 0:
                    await asyncio.sleep(60 * td.run_cnt)
                    
                t = asyncio.create_task(td.execute())
                running_tasks.add(t)
                t.add_done_callback(on_done)

            await asyncio.sleep(0.5)


def main():
    if len(sys.argv) != 2:
        print(f"USAGE: {sys.argv[0]} ids.txt", file = sys.stderr)
        sys.exit(2)

    id_file = sys.argv[1]
    ids = None
    with open(id_file) as f:
        ids = list(map(lambda _: _.strip("\n").strip("\r"), f))

    #asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(download_sequences(ids))


if __name__ == "__main__":
    main()
