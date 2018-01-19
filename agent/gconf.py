#encoding: utf-8
class Config(object):
    pass

# 获取代码运行位置 PROJECT_PATH
if __name__ == '__main__':
    import pathlib
    setattr(Config, 'PROJECT_PATH', pathlib.Path(__file__).absolute())
    print(getattr(Config, 'PROJECT_PATH'))