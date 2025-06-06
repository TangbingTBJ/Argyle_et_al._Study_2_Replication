#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 16 03:45:36 2025

@author: tbj
"""

import os
os.chdir('/Users/tbj/Graduate/QMSS/RA_work/enhance_predictability/')

from gen_prompts import *
import openai
import time
import pandas as pd
from tqdm import tqdm
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from tenacity import retry, stop_after_attempt, wait_random_exponential, RetryError


openai.api_key = ""

def do_query(prompt, engine, max_tokens):
    messages = [{"role": "user", "content": prompt}]
    response = openai.chat.completions.create(
        model=engine,
        messages=messages,
        temperature=0.7,
        max_tokens=max_tokens,
        top_p=1,
        logprobs=True,
        top_logprobs=5
    )
    text = response.choices[0].message.content.strip()
    match = re.search(r'^\d+', text)
    prediction = match.group(0) if match else text
    return prediction, response

# --- Parallel GPT calls using ThreadPoolExecutor ---
def gen_response(prompt_dict, engine, max_tokens, max_workers=2):
    results = {}
    
    for key, prompt_list in tqdm(prompt_dict.items(), desc="Processing keys"):
        key_responses = []
        
        time.sleep(0.3)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(do_query, prompt, engine, max_tokens): prompt
                for prompt in prompt_list
            }

            for future in tqdm(as_completed(futures), total=len(prompt_list), desc=f"Processing {key}", leave=False):
                try:
                    prediction, completion = future.result()
                except RetryError:
                    prediction, completion = None, None
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    prediction, completion = None, None
                
                key_responses.append((prediction, completion))

        results[key] = key_responses

    return results

def predict_and_append(short_long, model_name, sampled_dfs, max_tokens):
    k = gen_response(short_long, model_name, max_tokens)
    
    target_vars = ['attend_church', 'discuss_politics', 'political_interest']
    years = [2012, 2016, 2020]
    
    df_index_mapping = {}
    df_idx = 0
    for year in years:
        for target_var in target_vars:
            key = f"{target_var}_{year}"
            df_index_mapping[key] = df_idx
            df_idx += 1
    
    for key, responses in k.items():
       
        df_idx = df_index_mapping[key]
        df = sampled_dfs[df_idx]
        
        predictions = [pred for pred, _ in responses]
        completions = [comp for _, comp in responses]
        
        if len(predictions) != len(df):
            predictions = predictions[:len(df)] if len(predictions) > len(df) else predictions + [None] * (len(df) - len(predictions))
            completions = completions[:len(df)] if len(completions) > len(df) else completions + [None] * (len(df) - len(completions))
        
        df[model_name] = predictions
        df[f"{model_name}_completion"] = completions
        
        
#generate response for 10-variable predictions
model_name = 'gpt-3.5-turbo'   #'gpt-4o-mini' #'gpt-3.5-turbo'
short_long = llm_short_for_gpt
sampled_df_short_long = llm_short_sampled
predict_and_append(short_long, model_name, sampled_df_short_long,3)
model_name = 'gpt-4o-mini'   #'gpt-4o-mini' #'gpt-3.5-turbo'
predict_and_append(short_long, model_name, sampled_df_short_long,3)
for i, df in enumerate(llm_short_sampled):
    df.to_csv(f'short_{i}.csv', index=False)
    
#generate response for 20-variable predictions
model_name = 'gpt-3.5-turbo'   #'gpt-4o-mini' #'gpt-3.5-turbo'
short_long = llm_long_for_gpt
sampled_df_short_long = llm_long_sampled
predict_and_append(short_long, model_name, sampled_df_short_long,3)
model_name = 'gpt-4o-mini'   #'gpt-4o-mini' #'gpt-3.5-turbo'
predict_and_append(short_long, model_name, sampled_df_short_long,3)
for i, df in enumerate(llm_long_sampled):
    df.to_csv(f'long_{i}.csv', index=False)
    
