import time
import pandas as pd
import json
import os
from tqcenter import tq

class MarketSnapshotCSV:
    """
    全市场行情快照保存类
    用于获取所有市场行情快照并保存到CSV文件
    """

    def __init__(self, tdx_path=''):
        """
        初始化MarketSnapshotCSV类

        Args:
            tdx_path (str): 通达信安装路径，默认使用空字符串
        """
        # 初始化TQ数据接口
        try:
            tq.initialize(path=tdx_path)
            print(f"TQ数据接口初始化成功，使用路径: {tdx_path}")
        except Exception as e:
            print(f"TQ数据接口初始化失败: {e}")
            # 继续执行，后续方法会处理初始化失败的情况
            pass

    def get_all_stocks(self):
        """
        获取全市场股票列表

        Returns:
            list: 全市场股票代码列表，格式为['600000.SH', '000001.SZ', ...]
        """
        try:
            # 获取全市场股票列表
            stock_list = tq.get_stock_list()

            print(f"成功获取全市场股票列表，共{len(stock_list)}只股票")
            return stock_list
        except Exception as e:
            print(f"获取股票列表失败: {e}")
            return []

    def chunks(self, lst, n):
        """
        将列表分批处理

        Args:
            lst (list): 原始列表
            n (int): 每批大小

        Yields:
            list: 分批后的子列表
        """
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    def get_market_snapshot(self, batch_size=80):
        """
        获取全市场行情快照

        Args:
            batch_size (int): 每批处理的股票数量

        Returns:
            list: 所有股票的快照数据列表
        """
        # 获取全市场股票列表
        stock_list = self.get_all_stocks()
        if not stock_list:
            print("获取股票列表失败，无法获取行情快照")
            return []

        snapshots = []
        total_batches = (len(stock_list) + batch_size - 1) // batch_size
        current_batch = 0

        print(f"开始获取全市场行情快照，共{total_batches}批")

        # 分批获取行情数据
        for batch in self.chunks(stock_list, batch_size):
            current_batch += 1
            print(f"处理批次 {current_batch}/{total_batches}，股票数量: {len(batch)}")

            try:
                # 尝试逐个获取股票信息
                for stock_code in batch:
                    try:
                        # 使用get_market_snapshot获取股票行情快照
                        stock_snapshot = tq.get_market_snapshot(stock_code=stock_code)

                        if stock_snapshot and stock_snapshot.get('ErrorId') == '0':
                            # 构建快照数据字典
                            snapshot = {'code': stock_code}

                            # 处理数据格式
                            for field, value in stock_snapshot.items():
                                if field != 'ErrorId':
                                    snapshot[field] = value

                            snapshots.append(snapshot)
                            print(f"成功获取股票 {stock_code} 的快照信息")
                        else:
                            print(f"获取股票 {stock_code} 快照信息失败: {stock_snapshot}")
                    except Exception as e:
                        print(f"获取股票 {stock_code} 快照信息失败: {e}")
                        # 继续处理其他股票
                        continue
            except Exception as e:
                print(f"获取批次数据失败: {e}")
                # 继续处理下一批次
                continue

            # 每批次处理后休息一下，避免请求过于频繁
            time.sleep(0.5)

        print(f"全市场行情快照获取完成，成功获取 {len(snapshots)} 只股票的数据")
        return snapshots

    def save_snapshot_to_csv(self, snapshots, filename=None):
        """
        保存行情快照到CSV文件

        Args:
            snapshots (list): 行情快照数据列表
            filename (str): 保存文件名，默认使用当前时间

        Returns:
            str: 保存的文件路径
        """
        if not snapshots:
            print("行情快照数据为空，无法保存")
            return None

        # 生成文件名
        if not filename:
            import datetime
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'market_snapshot_{timestamp}.csv'

        # 创建DataFrame
        df = pd.DataFrame(snapshots)

        # 保存为CSV文件
        try:
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"行情快照已保存到CSV文件: {filename}")
            print(f"保存的股票数量: {len(df)}")
            return filename
        except Exception as e:
            print(f"保存行情快照失败: {e}")
            return None

    def save_snapshot_to_json(self, snapshots, filename=None):
        """
        保存行情快照到JSON文件

        Args:
            snapshots (list): 行情快照数据列表
            filename (str): 保存文件名，默认使用当前时间

        Returns:
            str: 保存的文件路径
        """
        if not snapshots:
            print("行情快照数据为空，无法保存")
            return None

        # 生成文件名
        if not filename:
            import datetime
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'market_snapshot_{timestamp}.json'

        # 保存为JSON文件
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(snapshots, f, ensure_ascii=False, indent=2)
            print(f"行情快照已保存到JSON文件: {filename}")
            print(f"保存的股票数量: {len(snapshots)}")
            return filename
        except Exception as e:
            print(f"保存行情快照到JSON失败: {e}")
            return None

    def run(self, batch_size=80):
        """
        运行完整的获取和保存流程

        Args:
            batch_size (int): 每批处理的股票数量

        Returns:
            tuple: (csv_file_path, json_file_path)
        """
        # 获取行情快照
        snapshots = self.get_market_snapshot(batch_size)

        # 保存到CSV和JSON
        csv_file = None
        json_file = None

        if snapshots:
            csv_file = self.save_snapshot_to_csv(snapshots)
            json_file = self.save_snapshot_to_json(snapshots)

        return csv_file, json_file

# 示例用法
if __name__ == "__main__":
    # 首先尝试关闭可能存在的TQ接口连接
    try:
        tq.close()
        print("已关闭之前的TQ数据接口连接")
    except Exception as e:
        print(f"关闭之前的TQ数据接口连接失败: {e}")

    # 初始化MarketSnapshotCSV实例
    # 使用通达信安装根目录作为路径
    tdx_root_path = "e:\\new_tdx64"
    print(f"使用通达信根目录作为路径: {tdx_root_path}")
    msc = MarketSnapshotCSV(tdx_path=tdx_root_path)

    # 运行完整流程
    print("开始获取全市场行情快照并保存到文件...")
    csv_file, json_file = msc.run(batch_size=80)

    if csv_file or json_file:
        print("\n操作完成！")
        if csv_file:
            print(f"行情快照已保存到CSV文件: {csv_file}")
        if json_file:
            print(f"行情快照已保存到JSON文件: {json_file}")
    else:
        print("\n操作失败，无法获取或保存行情快照")

    # 关闭TQ数据接口连接
    try:
        tq.close()
        print("TQ数据接口连接已关闭")
    except Exception as e:
        print(f"关闭TQ数据接口失败: {e}")
