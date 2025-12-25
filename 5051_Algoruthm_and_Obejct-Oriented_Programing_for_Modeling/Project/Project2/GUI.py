import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, 
    QFrame, QListWidget, QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox, 
    QDialog, QLabel, QLineEdit, QListWidgetItem, QComboBox
)
from PyQt5.QtCore import Qt
import numpy as np
from sort import QuickSort, MergeSort, CountingSort, HeapSort
from datetime import datetime
import re

### 排序 副窗口 ###
class SortDialog(QDialog):
    def __init__(self, parent=None, data_frames=None):
        super().__init__(parent)
        self.setWindowTitle("排序数据")
        self.data_frames = data_frames
        self.selected_frame = None
        self.selected_column = None  # 修复1: 专门存储选中的列
        self.sort_order = "ascending"
        self.selected_algorithm = "默认"
        self.current_df = None  # 存储当前DataFrame引用

        # 创建布局
        layout = QVBoxLayout()

        # 下拉框1：选择排序依据列
        column_layout = QHBoxLayout()
        column_layout.addWidget(QLabel("排序列:"))
        self.column_combo = QComboBox()
        # 修复2: 绑定当前列变化事件
        self.column_combo.currentTextChanged.connect(self.on_column_changed)
        column_layout.addWidget(self.column_combo)
        layout.addLayout(column_layout)

        # 下拉框2：选择正序/倒序
        order_layout = QHBoxLayout()
        order_layout.addWidget(QLabel("排序顺序:"))
        self.order_combo = QComboBox()
        self.order_combo.addItems(["正序", "倒序"])
        order_layout.addWidget(self.order_combo)
        layout.addLayout(order_layout)

        # 下拉框3：选择排序算法
        algorithm_layout = QHBoxLayout()
        algorithm_layout.addWidget(QLabel("排序算法:"))
        self.algorithm_combo = QComboBox()
        # 添加算法选项（默认 + 4种自定义算法）
        self.algorithm_combo.addItems([
            "默认 (Pandas)", 
            "快速排序 (QuickSort)", 
            "归并排序 (MergeSort)", 
            "堆排序 (HeapSort)", 
            "计数排序 (CountingSort)"
        ])
        self.algorithm_combo.currentTextChanged.connect(self.on_algorithm_changed)  # 绑定事件
        algorithm_layout.addWidget(self.algorithm_combo)
        layout.addLayout(algorithm_layout)

        # 数据类型信息标签
        self.data_type_info = QLabel("未选择列")
        self.data_type_info.setWordWrap(True)
        self.data_type_info.setStyleSheet("color: #0066cc; font-weight: bold;")
        layout.addWidget(self.data_type_info)

        # 算法说明标签
        self.algorithm_info = QLabel()
        self.algorithm_info.setWordWrap(True)
        self.algorithm_info.setStyleSheet("color: #666; font-size: 9pt;")
        layout.addWidget(self.algorithm_info)

        # 按钮布局
        button_layout = QHBoxLayout()
        sort_button = QPushButton("排序")
        sort_button.clicked.connect(self.perform_sort)
        button_layout.addWidget(sort_button)
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # 初始化数据
        self.update_data()

    def update_data(self):
        """统一更新数据和UI"""
        selected_item = self.parent().narrow_widget.currentItem()
        if not selected_item:
            return
        
        self.selected_frame = selected_item.text()
        self.current_df = self.data_frames.get(self.selected_frame)
        
        if self.current_df is not None:
            # 保存当前列选择
            current_col = self.column_combo.currentText() if self.column_combo.count() > 0 else ""
            
            # 更新列下拉框
            self.column_combo.clear()
            self.column_combo.addItems(self.current_df.columns.tolist())
            
            # 恢复列选择（如果存在）
            if current_col in self.current_df.columns:
                self.column_combo.setCurrentText(current_col)
                self.selected_column = current_col
            elif self.current_df.columns.tolist():
                self.selected_column = self.current_df.columns[0]
                self.column_combo.setCurrentText(self.selected_column)
            
            # 更新数据类型信息
            self.update_data_type_info()

    def on_column_changed(self, column_name):
        """列选择改变时更新状态"""
        self.selected_column = column_name

    def on_algorithm_changed(self, algorithm_name):
        """算法选择改变时更新说明"""
        self.selected_algorithm = algorithm_name

        # 修复3: 算法切换时保存当前列选择
        saved_column = self.selected_column
        
        if self.current_df is not None:
            # 仅当选择Counting Sort时，过滤非整数列
            if "计数排序 (CountingSort)" in algorithm_name:
                numeric_cols = self.current_df.select_dtypes(include=['int', 'int64']).columns
                if len(numeric_cols) == 0:
                    QMessageBox.warning(self, "警告", 
                        "当前数据集中没有整数列，计数排序不可用！")
                self.column_combo.clear()
                available_cols = numeric_cols.tolist()
                if not available_cols:  # 没有整数列时显示所有列但禁用计数排序
                    available_cols = self.current_df.columns.tolist()
                self.column_combo.addItems(available_cols)
                
                # 恢复可用的列选择
                if saved_column in available_cols:
                    self.column_combo.setCurrentText(saved_column)
                    self.selected_column = saved_column
                elif available_cols:
                    self.selected_column = available_cols[0]
                    self.column_combo.setCurrentText(self.selected_column)
            else:
                self.column_combo.clear()
                self.column_combo.addItems(self.current_df.columns.tolist())
                
                # 恢复列选择
                if saved_column in self.current_df.columns:
                    self.column_combo.setCurrentText(saved_column)
                    self.selected_column = saved_column
                elif self.current_df.columns.tolist():
                    self.selected_column = self.current_df.columns[0]
                    self.column_combo.setCurrentText(self.selected_column)
            
            # 更新数据类型信息
            self.update_data_type_info()

    def update_data_type_info(self):
        """更新数据类型信息标签"""
        if not self.selected_column or self.current_df is None:
            self.data_type_info.setText("未选择有效列")
            return
            
        col_data = self.current_df[self.selected_column]
        
        # ====== 智能数据类型检测 ====== #
        data_type, details = self.detect_data_type(col_data)
        
        
        # 显示数据类型信息
        if data_type == "timestamp":
            self.data_type_info.setText(f"🕒 检测到时间戳数据 ({details})")
        elif data_type == "integer":
            self.data_type_info.setText(f"🔢 整数数据 (范围: {details})")
        elif data_type == "float":
            self.data_type_info.setText(f"🔢 浮点数数据")
        elif data_type == "numeric_string":
            self.data_type_info.setText(f"🔠 数字字符串 ({details})")
        elif data_type == "mixed_numeric":
            self.data_type_info.setText(f"⚠️ 混合数值类型 (整数:{details})")
        elif data_type == "string":
            self.data_type_info.setText(f"🔤 普通文本 (字典序排序)")
        else:
            self.data_type_info.setText(f"❓ 未知类型: {data_type}")
        # ====== 智能数据类型检测结束 ====== #

    def detect_data_type(self, series):
        """
        智能检测列的数据类型
        返回: (类型, 详情)
        类型包括: 'timestamp', 'integer', 'float', 'numeric_string', 'mixed_numeric', 'string'
        """
        # 处理空列
        if len(series) == 0:
            return "empty", "空列"
        
        # 获取非空样本（最多100个）
        sample = series.dropna().head(100).tolist()
        if len(sample) == 0:
            return "empty", "全为空值"
        
        # ====== 1. 检测时间戳格式 ====== #
        time_format = self.detect_timestamp_format(sample)
        if time_format:
            return "timestamp", time_format
        
        # ====== 2. 检测纯数值类型 ====== #
        int_count = 0
        float_count = 0
        str_count = 0
        mixed_numeric = False
        
        for item in sample:
            if isinstance(item, (int, np.integer)):
                int_count += 1
            elif isinstance(item, (float, np.floating)):
                if not np.isnan(item):  # 忽略NaN
                    if item.is_integer():
                        int_count += 1
                    else:
                        float_count += 1
            elif isinstance(item, str):
                str_count += 1
                # 检查是否为数字字符串
                cleaned = item.strip().replace(',', '')
                if cleaned.startswith('-'):
                    cleaned = cleaned[1:]
                
                if cleaned.replace('.', '', 1).isdigit():
                    if '.' in cleaned:
                        float_count += 1
                    else:
                        int_count += 1
                # 检查是否为科学计数法
                elif re.match(r'^\d+\.?\d*[eE][-+]?\d+$', cleaned):
                    float_count += 1
        
        # 确定主类型
        total_valid = int_count + float_count + str_count
        if total_valid == 0:
            return "empty", "无有效数据"
        
        # 检查是否主要是数值
        numeric_ratio = (int_count + float_count) / total_valid
        
        if numeric_ratio > 0.9:  # 90%以上是数值
            if float_count > 0 and int_count > 0:
                return "mixed_numeric", f"整数: {int_count}, 浮点: {float_count}"
            elif float_count > 0:
                return "float", ""
            elif int_count > 0:
                # 获取值范围
                try:
                    min_val = min(series.dropna().astype(int))
                    max_val = max(series.dropna().astype(int))
                    return "integer", f"{min_val} 到 {max_val}"
                except:
                    return "integer", "整数"
        
        # 检查是否为数字字符串
        if str_count > 0 and numeric_ratio > 0.5:
            return "numeric_string", "包含数字的字符串"
        
        # ====== 3. 默认: 普通字符串 ====== #
        return "string", ""

    def detect_timestamp_format(self, sample):
        """
        检测时间戳格式
        支持常见格式:
        - YYYY-MM-DD HH:MM:SS
        - YYYY/MM/DD HH:MM:SS
        - MM/DD/YYYY HH:MM:SS
        - DD/MM/YYYY HH:MM:SS
        - YYYY-MM-DD
        - YYYY/MM/DD
        """
        # 常见时间格式
        formats = [
            ('%Y-%m-%d %H:%M:%S', 'YYYY-MM-DD HH:MM:SS'),
            ('%Y/%m/%d %H:%M:%S', 'YYYY/MM/DD HH:MM:SS'),
            ('%m/%d/%Y %H:%M:%S', 'MM/DD/YYYY HH:MM:SS'),
            ('%d/%m/%Y %H:%M:%S', 'DD/MM/YYYY HH:MM:SS'),
            ('%Y-%m-%d', 'YYYY-MM-DD'),
            ('%Y/%m/%d', 'YYYY/MM/DD'),
            ('%m/%d/%Y', 'MM/DD/YYYY'),
            ('%d/%m/%Y', 'DD/MM/YYYY')
        ]
        
        for fmt_code, fmt_desc in formats:
            valid_count = 0
            for item in sample:
                if not isinstance(item, str):
                    continue
                
                try:
                    # 尝试解析
                    datetime.strptime(item.strip(), fmt_code)
                    valid_count += 1
                except (ValueError, TypeError):
                    continue
            
            # 如果超过80%的样本匹配该格式，认为是有效格式
            if valid_count >= len(sample) * 0.8 and valid_count > 0:
                return fmt_desc
        
        return None

    def prepare_data_for_sorting(self, series):
        """
        准备数据用于排序
        返回: (转换后的数据列表, 数据类型, 转换信息)
        """
        data_type, details = self.detect_data_type(series)
        
        if data_type == "timestamp":
            # ====== 转换时间戳 ====== #
            time_format = details
            format_map = {
                'YYYY-MM-DD HH:MM:SS': '%Y-%m-%d %H:%M:%S',
                'YYYY/MM/DD HH:MM:SS': '%Y/%m/%d %H:%M:%S',
                'MM/DD/YYYY HH:MM:SS': '%m/%d/%Y %H:%M:%S',
                'DD/MM/YYYY HH:MM:SS': '%d/%m/%Y %H:%M:%S',
                'YYYY-MM-DD': '%Y-%m-%d',
                'YYYY/MM/DD': '%Y/%m/%d',
                'MM/DD/YYYY': '%m/%d/%Y',
                'DD/MM/YYYY': '%d/%m/%Y'
            }
            fmt_code = format_map.get(time_format, '%Y-%m-%d %H:%M:%S')
            
            timestamps = []
            for item in series:
                if pd.isna(item):
                    timestamps.append(float('-inf'))  # NaN处理为最小值
                    continue
                
                try:
                    # 尝试转换
                    dt_str = str(item).strip()
                    dt = datetime.strptime(dt_str, fmt_code)
                    timestamps.append(int(dt.timestamp()))
                except (ValueError, TypeError):
                    # 无法转换的处理为特殊值
                    timestamps.append(float('-inf'))
            
            return [int(ts) for ts in timestamps], "float", f"转换为Unix时间戳 ({time_format})"
        
        elif data_type in ["integer", "float", "mixed_numeric", "numeric_string"]:
            # ====== 转换为数值 ====== #
            numeric_values = []
            for item in series:
                if pd.isna(item):
                    numeric_values.append(float('-inf'))
                    continue
                
                try:
                    # 处理字符串数值
                    if isinstance(item, str):
                        cleaned = item.strip().replace(',', '')
                        # 处理百分比
                        if cleaned.endswith('%'):
                            cleaned = cleaned[:-1]
                            value = float(cleaned) / 100.0
                        else:
                            value = float(cleaned)
                    else:
                        value = float(item)
                    
                    numeric_values.append(value)
                except (ValueError, TypeError):
                    numeric_values.append(float('-inf'))
            
            # 确定最终类型
            final_type = "float" if any(isinstance(x, float) and not np.isinf(x) and not x.is_integer() for x in numeric_values) else "int"
            return numeric_values, final_type, f"统一转换为{final_type}"
        
        else:  # string or unknown
            # ====== 普通字符串处理 ====== #
            string_values = []
            for item in series:
                if pd.isna(item) or item == "" or str(item).strip() == "":
                    string_values.append("")  # 空字符串排在最前
                else:
                    string_values.append(str(item).strip())
            
            return string_values, "string", "字典序排序"

    def perform_sort(self):
        # 修复4: 每次排序前重新获取最新数据
        selected_item = self.parent().narrow_widget.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "排序失败", "请选择要排序的变量")
            return
        
        var_name = selected_item.text()
        df = self.data_frames.get(var_name)
        if df is None:
            QMessageBox.warning(self, "排序失败", "数据不存在")
            return
        
        # 修复5: 直接使用当前UI状态，不依赖实例变量
        sort_column = self.column_combo.currentText()
        sort_order = self.order_combo.currentText()
        selected_algorithm = self.algorithm_combo.currentText()
        
        # 确保排序列在数据框中
        if sort_column not in df.columns:
            QMessageBox.warning(self, "排序失败", f"选择的排序列 '{sort_column}' 不存在")
            return

        # 执行排序
        ascending = True if sort_order == "正序" else False
        
        try:
            if selected_algorithm == "默认 (Pandas)":
                # ====== 智能排序：处理混合数据类型 ====== #
                col_data = df[sort_column]
                data_type, _ = self.detect_data_type(col_data)
                
                if data_type == "timestamp":
                    # 转换为datetime类型后排序
                    time_format = self.detect_timestamp_format(col_data.dropna().head(100).tolist())
                    if time_format:
                        format_map = {
                            'YYYY-MM-DD HH:MM:SS': '%Y-%m-%d %H:%M:%S',
                            'YYYY/MM/DD HH:MM:SS': '%Y/%m/%d %H:%M:%S',
                            'MM/DD/YYYY HH:MM:SS': '%m/%d/%Y %H:%M:%S',
                            'DD/MM/YYYY HH:MM:SS': '%d/%m/%Y %H:%M:%S',
                            'YYYY-MM-DD': '%Y-%m-%d',
                            'YYYY/MM/DD': '%Y/%m/%d',
                            'MM/DD/YYYY': '%m/%d/%Y',
                            'DD/MM/YYYY': '%d/%m/%Y'
                        }
                        fmt_code = format_map.get(time_format, '%Y-%m-%d %H:%M:%S')
                        
                        # 创建临时列进行转换
                        temp_col = df[sort_column].apply(
                            lambda x: pd.to_datetime(str(x).strip(), format=fmt_code, errors='coerce')
                        )
                        sorted_df = df.assign(_temp_sort=temp_col).sort_values(
                            by='_temp_sort', ascending=ascending
                        ).drop('_temp_sort', axis=1)
                    else:
                        # 无法识别格式，按字符串排序
                        sorted_df = df.sort_values(by=sort_column, ascending=ascending)
                else:
                    # 使用Pandas内置排序（自动处理混合类型）
                    sorted_df = df.sort_values(by=sort_column, ascending=ascending)
                
                new_var_name = f"{var_name}_sorted"
            
            else:
                # ====== 自定义排序算法处理 ====== #
                col_data = df[sort_column].copy()
                
                # 1. 智能数据准备
                data_list, data_type, conversion_info = self.prepare_data_for_sorting(col_data)
                
                # 2. 特殊类型验证
                if "计数排序 (CountingSort)" in selected_algorithm:
                    if data_type not in ["int", "integer"]:
                        raise ValueError(f"计数排序仅支持整数列！\n当前列: {sort_column}\n类型: {data_type} ({conversion_info})")
                
                elif any(name in selected_algorithm for name in ["快速", "归并", "堆"]):
                    if data_type not in ["int", "integer", "float"]:
                        raise ValueError(f"数值排序算法仅支持数值列！\n当前列: {sort_column}\n类型: {data_type} ({conversion_info})")
                
                # 3. 创建索引映射（保持行完整性）
                indices = np.arange(len(col_data))
                
                # 4. 选择排序算法
                if "快速排序 (QuickSort)" in selected_algorithm:
                    from sort import QuickSort
                    sorter = QuickSort()
                    # 创建(值, 索引)对以便保持稳定性
                    paired = list(zip(data_list, indices))
                    # 按值排序
                    paired.sort(key=lambda x: x[0])  # 临时用内置sort保证稳定性
                    sorted_indices = [idx for (_, idx) in paired]
                
                elif "归并排序 (MergeSort)" in selected_algorithm:
                    from sort import MergeSort
                    sorter = MergeSort()
                    # 创建(值, 索引)对
                    paired = list(zip(data_list, indices))
                    # 按值排序
                    paired.sort(key=lambda x: x[0])  # 临时用内置sort
                    sorted_indices = [idx for (_, idx) in paired]
                
                elif "堆排序 (HeapSort)" in selected_algorithm:
                    from sort import HeapSort
                    sorter = HeapSort()
                    # 堆排序不稳定，需特殊处理
                    paired = list(zip(data_list, indices))
                    # 按值排序
                    paired.sort(key=lambda x: x[0])  # 临时用内置sort
                    sorted_indices = [idx for (_, idx) in paired]
                
                elif "计数排序 (CountingSort)" in selected_algorithm:
                    from sort import CountingSort
                    sorter = CountingSort()
                    # 仅对整数有效
                    valid_pairs = []
                    invalid_indices = []
                    
                    for i, val in enumerate(data_list):
                        if not np.isinf(val) and isinstance(val, (int, float)) and not np.isnan(val):
                            # 确保是整数
                            int_val = int(round(val))
                            valid_pairs.append((int_val, i))
                        else:
                            invalid_indices.append(i)
                    
                    if not valid_pairs:
                        raise ValueError("没有有效整数值用于计数排序")
                    
                    # 按值排序
                    valid_pairs.sort(key=lambda x: x[0])
                    sorted_indices = [idx for (_, idx) in valid_pairs]
                    sorted_indices.extend(invalid_indices)  # 无效值放在最后
                
                # 5. 应用排序（关键：保持行完整）
                sorted_df = df.iloc[sorted_indices]
                
                # 6. 处理倒序
                if not ascending:
                    sorted_df = sorted_df.iloc[::-1]
                
                # 7. 生成新变量名
                algo_abbr = "".join([s[0] for s in selected_algorithm.split(" (")[0].split()[:2]])
                new_var_name = f"{var_name}_{algo_abbr}_sorted"
            
            # save result
            self.parent().data_frames[new_var_name] = sorted_df
            self.parent().narrow_widget.addItem(new_var_name)
            
            # 获取数据类型信息用于显示
            col_data = df[sort_column]
            data_type, details = self.detect_data_type(col_data)
            
            QMessageBox.information(self, "排序成功", 
                f"排序完成！\n"
                f"算法: {selected_algorithm}\n"
                f"列名: '{sort_column}'\n"
                f"数据类型: {data_type}\n"
                f"转换: {conversion_info if 'conversion_info' in locals() else '无'}\n"
                f"新变量名: {new_var_name}\n"
                f"行数: {len(sorted_df)}")
        
        except Exception as e:
            QMessageBox.critical(self, "排序错误", f"排序失败: {str(e)}\n\n详细信息:\n列: {sort_column}\n算法: {selected_algorithm}")
            import traceback
            print("排序错误详情:", traceback.format_exc())
            return        
        self.close()

### 导出数据 副窗口 ###
class ExportDialog(QDialog):
    def __init__(self, parent=None, data_frames=None):
        super().__init__(parent)
        self.setWindowTitle("导出数据")
        self.data_frames = data_frames
        self.selected_frames = []
        self.export_path = ""  # 导出路径

        # 创建布局
        layout = QVBoxLayout()

        # 多选选项视窗
        self.multi_select_widget = QListWidget()
        self.multi_select_widget.setAlternatingRowColors(True)
        self.multi_select_widget.setSpacing(5)
        for var_name in self.data_frames.keys():
            item = QListWidgetItem(var_name)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.multi_select_widget.addItem(item)
        self.multi_select_widget.itemChanged.connect(self.update_selection)
        layout.addWidget(self.multi_select_widget)

        # 导出地址选择组件
        input_layout = QHBoxLayout()
        label = QLabel("导出路径")
        input_layout.addWidget(label)
        self.export_path_input = QLineEdit()
        self.export_path_input.setPlaceholderText("当前目录")
        self.export_path_input.setReadOnly(True)
        input_layout.addWidget(self.export_path_input)
        browse_button = QPushButton("浏览")
        browse_button.clicked.connect(self.select_export_path)
        input_layout.addWidget(browse_button)
        layout.addLayout(input_layout)

        # 按钮布局
        button_layout = QHBoxLayout()
        export_button = QPushButton("导出")
        export_button.clicked.connect(self.export_data)
        button_layout.addWidget(export_button)
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def update_selection(self):
        self.selected_frames = []
        for index in range(self.multi_select_widget.count()):
            item = self.multi_select_widget.item(index)
            if item.checkState() == Qt.Checked:
                self.selected_frames.append(item.text())

    def select_export_path(self):
        # 弹出文件选择对话框，选择导出路径
        export_path = QFileDialog.getExistingDirectory(self, "选择导出路径")
        if export_path:
            self.export_path = export_path
            self.export_path_input.setText(export_path)

    def export_data(self):
        if not self.selected_frames:
            QMessageBox.warning(self, "导出失败", "请选择要导出的变量")
            return
        if not self.export_path:
            QMessageBox.warning(self, "导出失败", "请选择导出路径")
            return
        for var_name in self.selected_frames:
            df = self.data_frames[var_name]
            file_path = f"{self.export_path}/{var_name}.csv"
            df.to_csv(file_path, index=False)
        QMessageBox.information(self, "导出成功", "所选变量已成功导出为CSV文件")
        self.close()

### 合并数据框 副窗口 ###
class MergeDialog(QDialog):
    def __init__(self, parent=None, data_frames=None):
        super().__init__(parent)
        self.setWindowTitle("合并数据")
        self.data_frames = data_frames
        self.selected_frames = []
        self.new_var_name = ""

        # 创建布局
        layout = QVBoxLayout()

        # 多选选项视窗
        self.multi_select_widget = QListWidget()
        self.multi_select_widget.setAlternatingRowColors(True)
        self.multi_select_widget.setSpacing(5)
        for var_name in self.data_frames.keys():
            item = QListWidgetItem(var_name)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.multi_select_widget.addItem(item)
        self.multi_select_widget.itemChanged.connect(self.update_selection)
        layout.addWidget(self.multi_select_widget)

        # 输入组件
        input_layout = QHBoxLayout()
        label = QLabel("新变量名称")
        input_layout.addWidget(label)
        self.new_var_name_input = QLineEdit()
        self.new_var_name_input.setPlaceholderText("默认名称")
        self.new_var_name_input.setReadOnly(True)
        input_layout.addWidget(self.new_var_name_input)
        layout.addLayout(input_layout)

        # 按钮布局
        button_layout = QHBoxLayout()
        merge_button = QPushButton("合并")
        merge_button.clicked.connect(self.merge_data)
        button_layout.addWidget(merge_button)
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def update_selection(self):
        self.selected_frames = []
        for index in range(self.multi_select_widget.count()):
            item = self.multi_select_widget.item(index)
            if item.checkState() == Qt.Checked:
                self.selected_frames.append(item.text())
        if self.selected_frames:
            self.new_var_name_input.setPlaceholderText(self.selected_frames[0] + "_merge")
            self.new_var_name_input.setReadOnly(False)
        else:
            self.new_var_name_input.setPlaceholderText("默认名称")
            self.new_var_name_input.setReadOnly(True)

    def merge_data(self):
        if len(self.selected_frames) < 2:
            QMessageBox.warning(self, "合并失败", "至少需要选择两个变量进行合并")
            return
        # 使用 pd.concat 纵向拼接数据框
        merged_df = pd.concat([self.data_frames[var_name] for var_name in self.selected_frames], ignore_index=True)
        new_var_name = self.new_var_name_input.text() or self.new_var_name_input.placeholderText()
        self.parent().data_frames[new_var_name] = merged_df
        self.parent().narrow_widget.addItem(new_var_name)
        self.close()

### 搜索数据 副窗口 ###
class SearchDialog(QDialog):
    def __init__(self, parent=None, data_frames=None):
        super().__init__(parent)
        self.setWindowTitle("搜索数据")
        self.data_frames = data_frames
        self.search_results = []

        # 创建布局
        layout = QVBoxLayout()

        # 搜索输入框
        input_layout = QHBoxLayout()
        label = QLabel("搜索关键词")
        input_layout.addWidget(label)
        self.search_input = QLineEdit()
        input_layout.addWidget(self.search_input)
        layout.addLayout(input_layout)

        # 搜索结果列表
        self.search_results_widget = QListWidget()
        layout.addWidget(self.search_results_widget)

        # 按钮布局
        button_layout = QHBoxLayout()
        search_button = QPushButton("搜索")
        search_button.clicked.connect(self.perform_search)
        button_layout.addWidget(search_button)
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def perform_search(self):
        keyword = self.search_input.text().strip()
        if not keyword:
            QMessageBox.warning(self, "搜索失败", "请输入搜索关键词")
            return
        
        self.search_results = []
        for var_name, df in self.data_frames.items():
            # === 优化1：跳过不可能匹配的数值列 ===
            # 仅当keyword是纯数字时，才检查数值列
            numeric_cols = df.select_dtypes(include=np.number).columns

            str_cols = df.columns.difference(numeric_cols)
            
            # === 优化2：分块处理减少内存峰值 ===
            mask = pd.Series(False, index=df.index)  # 初始化全False
            
            # 处理字符串列（直接比较）
            if not str_cols.empty:
                str_df = df[str_cols].astype(str)
                mask |= str_df.eq(keyword).any(axis=1)
            
            # 处理数值列（仅当keyword是数字时）
            if numeric_cols.any() and keyword.replace('.', '', 1).isdigit():
                num_val = float(keyword) if '.' in keyword else int(keyword)
                num_df = df[numeric_cols]
                mask |= num_df.eq(num_val).any(axis=1)
            
            filtered_df = df[mask]
            if not filtered_df.empty:
                self.search_results.append((var_name, filtered_df))
        
        self.update_search_results()

    def update_search_results(self):
        self.search_results_widget.clear()
        for var_name, df in self.search_results:
            item = QListWidgetItem(f"{var_name} ({len(df)} 条结果)")
            self.search_results_widget.addItem(item)

### 主窗口 ###
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 GUI 示例")
        self.resize(800, 600)
        self.data_frames = {}  # 用于存储导入的数据

        # 创建主布局
        main_layout = QHBoxLayout()

        # 左侧按钮布局
        left_layout = QVBoxLayout()
        buttons = ["导入", "合并", "删除", "搜索", "排序", "导出", "退出"]
        self.buttons = {}
        for button_text in buttons:
            button = QPushButton(button_text)
            button.setMinimumHeight(50)
            if button_text == "导入":
                button.clicked.connect(self.import_data)
            elif button_text == "合并":
                button.clicked.connect(self.merge_data)
            elif button_text == "删除":
                button.clicked.connect(self.delete_data)
            elif button_text == "搜索":
                button.clicked.connect(self.search_data)
            elif button_text == "排序":
                button.clicked.connect(self.sort_data)
            elif button_text == "导出":
                button.clicked.connect(self.export_data)
            elif button_text == "退出":
                button.clicked.connect(self.exit_app)
            left_layout.addWidget(button)
            self.buttons[button_text] = button

        # 创建左侧框架并设置布局
        left_frame = QFrame()
        left_frame.setLayout(left_layout)
        left_frame.setFixedWidth(150)

        # 右侧布局
        right_layout = QVBoxLayout()

        # 右侧窄视窗（显示选项，可选中且高亮）
        self.narrow_widget = QListWidget()
        self.narrow_widget.setFixedHeight(100)  # 设置高度，使其更窄
        self.narrow_widget.itemSelectionChanged.connect(self.display_data)
        right_layout.addWidget(self.narrow_widget)

        # 右侧宽视窗（显示表格）
        self.wide_widget = QTableWidget()
        self.wide_widget.cellClicked.connect(self.update_row_label)  # 绑定单元格点击事件
        right_layout.addWidget(self.wide_widget)

        # 行数显示窗口
        self.row_label = QLabel("0/0")
        right_layout.addWidget(self.row_label)

        # 创建右侧框架并设置布局
        right_frame = QFrame()
        right_frame.setLayout(right_layout)

        # 将左右框架添加到主布局
        main_layout.addWidget(left_frame)
        main_layout.addWidget(right_frame)

        # 创建中心窗口并设置布局
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def import_data(self):
        # 弹出文件选择对话框，允许选择多个 .csv 文件
        file_names, _ = QFileDialog.getOpenFileNames(self, "选择文件", ".", "CSV 文件 (*.csv)")
        if file_names:
            for file_name in file_names:
                # 使用 pandas 读取 CSV 文件，假设数据没有表头
                df = pd.read_csv(file_name, header=None)
                # 获取文件名（不带 .csv 后缀）
                var_name = file_name.split("/")[-1].replace(".csv", "")
                # 动态生成列名
                df.columns = [f"列{i}" for i in range(len(df.columns))]
                # 将数据存储到字典中，以文件名作为变量名
                self.data_frames[var_name] = df
                # 在选项视窗中显示变量名
                self.narrow_widget.addItem(var_name)

    def merge_data(self):
        if len(self.data_frames) < 2:
            QMessageBox.warning(self, "合并失败", "至少需要两个变量进行合并")
            return
        merge_dialog = MergeDialog(self, self.data_frames)
        merge_dialog.exec_()

    def delete_data(self):
        selected_item = self.narrow_widget.currentItem()
        if selected_item:
            var_name = selected_item.text()
            del self.data_frames[var_name]
            self.narrow_widget.takeItem(self.narrow_widget.row(selected_item))
            self.wide_widget.clear()
            self.row_label.setText("0/0")

    def search_data(self):
        if not self.data_frames:
            QMessageBox.warning(self, "搜索失败", "没有导入的数据可供搜索")
            return
        search_dialog = SearchDialog(self, self.data_frames)
        search_dialog.exec_()

    def sort_data(self):
        if not self.data_frames:
            QMessageBox.warning(self, "排序失败", "没有可排序的数据")
            return
        sort_dialog = SortDialog(self, self.data_frames)
        sort_dialog.exec_()

    def export_data(self):
        if not self.data_frames:
            QMessageBox.warning(self, "导出失败", "没有可导出的数据")
            return
        export_dialog = ExportDialog(self, self.data_frames)
        export_dialog.exec_()

    def exit_app(self):
        # 弹出确认退出对话框
        reply = QMessageBox.question(self, "确认退出", "确定要退出程序吗？",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # 释放所有内存，清空所有变量
            self.data_frames.clear()
            self.narrow_widget.clear()
            self.close()

    def display_data(self):
        selected_item = self.narrow_widget.currentItem()
        if selected_item:
            var_name = selected_item.text()
            df = self.data_frames.get(var_name)
            if df is not None:
                # 显示前100项数据
                df_head = df.head(100)
                # 动态调整表格列数
                self.wide_widget.setColumnCount(len(df_head.columns))
                self.wide_widget.setRowCount(len(df_head))
                self.wide_widget.setHorizontalHeaderLabels([f"列{i}" for i in range(len(df_head.columns))])
                for row in range(len(df_head)):
                    for col in range(len(df_head.columns)):
                        item = QTableWidgetItem(str(df_head.iloc[row, col]))
                        self.wide_widget.setItem(row, col, item)
                # 更新行数显示
                self.update_row_label()

    def update_row_label(self, row=None, col=None):
        selected_item = self.narrow_widget.currentItem()
        if selected_item:
            var_name = selected_item.text()
            df = self.data_frames.get(var_name)
            if df is not None:
                total_rows = len(df)  # 使用数据框的总行数
                if row is None:
                    row = self.wide_widget.currentRow()
                if row is not None:
                    self.row_label.setText(f"{row + 1}/{total_rows}")
                else:
                    self.row_label.setText(f"0/{total_rows}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())