# Copyright (c) 2024, Zhendong Peng (pzd17@tsinghua.org.cn)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import click
import os, csv, warnings
from pyvisqol import Visqol
from tqdm import tqdm

warnings.filterwarnings("ignore", category=UserWarning)

@click.command()
@click.argument("reference", type=click.Path(exists=True, file_okay=True))
@click.argument("defraded", type=click.Path(exists=True, file_okay=True))
@click.option("--output_csv", type=click.Path(file_okay=True), default=None, help="Optional output CSV file path.")

def main(reference, defraded, output_csv):
    visqol = Visqol()
    
    if output_csv:
        if not (os.path.isdir(reference) and os.path.isdir(defraded)):
            print("Error: 如果提供 output_csv 参数, reference 和 defraded 必须是文件夹")
            return
        files = os.listdir(reference)  # 获取参考文件夹中的所有文件
        total_files = len(files)       # 总文件数
        moslqo_scores = []


        # 打开 CSV 文件并准备写入
        with open(output_csv, mode="w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["File Name", "MOS-LQO"])  # 写入表头

    
            # 遍历参考文件夹中的所有文件
            # for ref_file in os.listdir(reference):
            for ref_file in tqdm(files, desc="MOS-LQO", total=total_files):
                ref_path = os.path.join(reference, ref_file)
                # 假设退化文件夹中的对应文件与参考文件的文件名一致
                deg_path = os.path.join(defraded, ref_file)

                # 确保退化文件存在
                if os.path.exists(deg_path):
                    moslqo = visqol.measure(ref_path, deg_path)
                    # print(f"{ref_file} - MOSLQO: {moslqo}")
                    moslqo_scores.append(moslqo)
                    writer.writerow([ref_file, moslqo])
                    csv_file.flush()
                else:
                    print(f"对应的退化文件未找到：{deg_path}")
    
        # 计算平均 MOS-LQO 值
        if moslqo_scores:
            average_moslqo = sum(moslqo_scores) / len(moslqo_scores)
            print(f"Average MOS-LQO : {average_moslqo:.14f}")
        else:
            print("没有 MOS-LQO 分数可供计算平均值")

    else:
        if os.path.isfile(reference) and os.path.isfile(defraded):
            moslqo = visqol.measure(reference, defraded)
            print(f"MOS-LQO: {moslqo}")
        else:
            print("Error: 如果未提供 output_csv 参数, reference 和 defraded 必须是单个文件")
        # moslqo = Visqol().measure(reference, defraded)
        # print(moslqo)


if __name__ == "__main__":
    main()
