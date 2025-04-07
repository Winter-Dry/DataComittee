import os, sys
from typing import Dict, List, Union
from collections import defaultdict


class RuleBasedPrompt:
    def __init__(self,
                 rules: Union[dict, list] = {},
                 prompt_head: str = '',
                 prompt_rule_body: str = '',
                 prompt_tail: str = '',
                 rule_part_keywords: list = []
                 ):
        self.rules = rules
        self.prompt_head = prompt_head
        self.prompt_rule_body = prompt_rule_body
        self.prompt_tail = prompt_tail
        self.rule_part_keywords = rule_part_keywords
        self.assembled_prompt = None

    def __call__(self):
        raise NotImplementedError

    def __str__(self):
        if self.assembled_prompt is None:
            if isinstance(self.rules, list):
                assembled_rule_prompt = self.prompt_rule_body.format('\n'.join(self.rules))
                self.assembled_prompt = '\n'.join([self.prompt_head, assembled_rule_prompt, self.prompt_tail])
            else:
                # todo rule_part_keywords = []
                parts = defaultdict(str)
                parts_idx = {k: 1 for k in self.rule_part_keywords}  # todo 编号自定义
                for idx, (k, v) in enumerate(self.rules.items()):
                    miss_flag = True
                    for i, keyword in enumerate(self.rule_part_keywords):
                        if keyword in k:
                            miss_flag = False
                            parts[keyword] += '''{}. **{}** : \n{}\n'''.format(parts_idx[keyword], k, v)
                            parts_idx[keyword] += 1
                            break
                    if miss_flag:
                        print('Missed rule: ', k, v)
                assembled_rule_prompt = self.prompt_rule_body.format(**parts)
                self.assembled_prompt = '\n'.join([self.prompt_head, assembled_rule_prompt, self.prompt_tail])

        return self.assembled_prompt


if __name__ == '__main__':
    prompt = RuleBasedPrompt(
        neg_define,
        prompt_rule_body=neg_prompt_template,
        rule_part_keywords=['正向', '负向', '中性']
    )

    print(str(prompt))