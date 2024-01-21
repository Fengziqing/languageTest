import os
"""
替换返回的翻译（未完成）
"""
def replace_content(L10n_path,translatedPath):
    if not os.path.exists(L10n_path):
        print('Your local Language file not exist at path: ' + L10n_path)
        return
    if not os.path.exists(translatedPath):
        print('Your translated file not exist at path: ' + translatedPath)
        return
    content = ''
    with open(translatedPath, 'r') as file:
        content = file.read()

    with open(L10n_path, 'w') as file:
        file.write(content)

if __name__ == '__main__':
    translatedPath = ''
    l10n_path = '/Users/haru.feng/Documents/SourceCode/ep-new-release/mac-client/Zoom/Zoom/Zoom'
    replace_content(l10n_path,translatedPath)