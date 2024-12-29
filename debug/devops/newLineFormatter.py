import os

def replace_crlf_with_lf_in_sh_files(directory):
    """
    遍历指定目录及所有层级的子目录，将 .sh 文件中的 \r\n 替换为 \n。
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".sh"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "rb") as f:
                        content = f.read()
                    # 替换 \r\n 为 \n
                    updated_content = content.replace(b'\r\n', b'\n')
                    # 写回文件
                    with open(file_path, "wb") as f:
                        f.write(updated_content)
                    print(f"Processed: {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    directory = r"C:\Users\kwz50\IdeaProjects\PowerBarcoder"
    if os.path.isdir(directory):
        replace_crlf_with_lf_in_sh_files(directory)
        print("处理完成！")
    else:
        print("输入的路径无效，请提供一个有效的目录路径。")
