#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
二进制文件转C数组格式转换器
将二进制文件转换为C语言unsigned char数组格式
"""

import sys
import os
import argparse

def binary_to_c_array(data, array_name="buf", bytes_per_line=12):
    """
    将二进制数据转换为C语言数组格式（字符串连接方式）
    
    Args:
        data: 二进制数据
        array_name: 数组变量名
        bytes_per_line: 每行显示的字节数
    
    Returns:
        str: C语言数组格式的字符串
    """
    if not data:
        return f"unsigned char {array_name}[] = \"\";"
    
    # 生成十六进制字符串列表（大写）
    hex_values = [f"\\x{byte:02X}" for byte in data]
    
    # 构建输出
    output = []
    output.append(f"unsigned char {array_name}[] =")
    
    # 按行分组输出
    for i in range(0, len(hex_values), bytes_per_line):
        line_values = hex_values[i:i + bytes_per_line]
        line_content = "".join(line_values)
        
        if i == 0:
            # 第一行
            line = f"    \"{line_content}\""
        else:
            # 后续行，使用字符串连接
            line = f"    \"{line_content}\""
        
        # 如果不是最后一行，不需要分号
        output.append(line)
    
    # 添加结尾分号
    output[-1] += ";"
    
    # 添加数组长度注释
    output.append(f"/* Length: {len(data)} bytes */")
    
    return "\n".join(output)

def binary_to_c_array_multiline(data, array_name="buf", bytes_per_line=12):
    """
    将二进制数据转换为多行C语言数组格式（使用0x格式）
    
    Args:
        data: 二进制数据
        array_name: 数组变量名
        bytes_per_line: 每行显示的字节数
    
    Returns:
        str: C语言数组格式的字符串
    """
    if not data:
        return f"unsigned char {array_name}[] = {{}};"
    
    output = []
    output.append(f"unsigned char {array_name}[] = {{")
    
    for i in range(0, len(data), bytes_per_line):
        line_data = data[i:i + bytes_per_line]
        hex_values = [f"0x{byte:02X}" for byte in line_data]
        
        # 添加缩进
        line = "    " + ", ".join(hex_values)
        
        # 如果不是最后一行，添加逗号
        if i + bytes_per_line < len(data):
            line += ","
        
        output.append(line)
    
    output.append("};")
    output.append(f"/* Length: {len(data)} bytes */")
    
    return "\n".join(output)

def read_binary_file(file_path):
    """
    读取二进制文件
    
    Args:
        file_path: 文件路径
    
    Returns:
        bytes: 文件内容
    """
    try:
        with open(file_path, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        print(f"错误: 文件 '{file_path}' 不存在")
        sys.exit(1)
    except PermissionError:
        print(f"错误: 没有权限读取文件 '{file_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"错误: 读取文件时发生异常: {e}")
        sys.exit(1)

def write_output(content, output_file):
    """
    写入输出文件
    
    Args:
        content: 要写入的内容
        output_file: 输出文件路径
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"成功写入到文件: {output_file}")
    except Exception as e:
        print(f"错误: 写入文件时发生异常: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='将二进制文件转换为C语言unsigned char数组格式',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例用法:
  %(prog)s file.bin                          # 转换文件，默认输出到out.txt
  %(prog)s file.bin -o result.h              # 指定输出文件
  %(prog)s file.bin -n data                  # 指定数组名为data
  %(prog)s file.bin -w 8                     # 每行8个字节
  %(prog)s file.bin --hex-format             # 使用0x格式而不是\\x格式
  %(prog)s file.bin --preview                # 预览输出不写入文件

输出格式示例:
  默认格式 (\\x 字符串连接):
    unsigned char buf[] =
        "\\x7F\\x45\\x4C\\x46\\x02\\x01\\x01\\x00\\x00\\x00\\x00\\x00"
        "\\x00\\x00\\x00\\x00";
  
  十六进制格式 (0x 数组):
    unsigned char buf[] = {
        0x7F, 0x45, 0x4C, 0x46, 0x02, 0x01, 0x01, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
    };
        '''
    )
    
    parser.add_argument('file', help='要转换的二进制文件路径')
    parser.add_argument('-o', '--output', default='out.txt', metavar='FILE',
                       help='输出文件路径 (默认: out.txt)')
    parser.add_argument('-n', '--name', default='buf', metavar='NAME',
                       help='数组变量名 (默认: buf)')
    parser.add_argument('-w', '--width', type=int, default=12, metavar='WIDTH',
                       help='每行显示的字节数 (默认: 12)')
    parser.add_argument('--hex-format', action='store_true',
                       help='使用0x格式代替\\x格式 (数组格式)')
    parser.add_argument('--preview', action='store_true',
                       help='预览输出内容，不写入文件')
    
    args = parser.parse_args()
    
    # 检查文件是否存在
    if not os.path.isfile(args.file):
        print(f"错误: '{args.file}' 不是一个有效的文件")
        sys.exit(1)
    
    # 读取文件数据
    print(f"读取文件: {args.file}")
    data = read_binary_file(args.file)
    file_size = len(data)
    print(f"文件大小: {file_size} 字节")
    
    # 生成C数组格式
    if args.hex_format:
        c_array = binary_to_c_array_multiline(data, args.name, args.width)
    else:
        c_array = binary_to_c_array(data, args.name, args.width)
    
    # 预览或写入文件
    if args.preview:
        print("\n预览输出:")
        print("-" * 50)
        print(c_array)
    else:
        write_output(c_array, args.output)
        print(f"数组名: {args.name}")
        print(f"数组长度: {file_size} 字节")

if __name__ == "__main__":
    main()