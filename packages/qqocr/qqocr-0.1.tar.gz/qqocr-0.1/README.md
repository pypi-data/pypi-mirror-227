# DDTank

A package used for writing ddtank game scripts.

Contact the author: jugking6688@gmail.com 

Video tutorial in bilibili: https://space.bilibili.com/3493127383943735

Examples are as follows：
```python
from ddtank import Status, get_game

class ScriptStatus(Status):
    def task(self):
        while True:
            self.press('B')

if __name__ == '__main__':
    handle_list = get_game()
    handle = handle_list[0]
    my_status = ScriptStatus(handle)
    my_status.start()
    my_status.stop()
```
---
# DDTank 非正式文档
#### Document for ddtank package

## 写在前面
> 本软件包的更新、规范全凭作者个人喜好而变动，请慎重使用！
>
> 作者邮箱: jugking6688@gmail.com 
> 
> B站视频系列： https://space.bilibili.com/3493127383943735
> 
> QQ交流群：285669805

---
## 版本更新说明 
* **version 1.1**

引入了图形化界面，即脚本执行器**ddtanker**。
```python
from ddtank import DDTanker

ddtanker = DDTanker()
```
    ddtanker有找色、截图、地图识别等功能，大大提高脚本编写的效率。
    注意，如果你想编写一个ddtanker能够识别、执行的ddtank脚本，你需要将子类命名为ScriptStatus，
    然后将.py文件放在./script文件夹中。
```python
from ddtank import Status

class ScriptStatus(Status):
    def task(self):
        self.click('rfind', pos=(520, 57), rgb=(6, 104, 210))
        self.click('rfind', pos=(743, 141), rgb=(247, 75, 61))
        self.click('rfind', pos=(430, 278), rgb=(149, 86, 92))
        self.sleep(100)
        self.click('rfind', pos=(241, 373), rgb=(83, 244, 52))
```
    一个能供ddtanker识别、执行的ddtank脚本，它的作用是：
    假设人物位于大厅，他将会进入农场，然后扭蛋一次。
---
## 1. 获取游戏窗口信息 get_game()
```python
from ddtank import get_game

hwnds = get_game()
```
上面的代码演示了如何获取当前已经运行了的，所有的**弹弹堂**游戏窗口的句柄，并保存到了列表hwnds中。

    get_game()的本质就是遍历所有1000*600的，类名为'MacromediaFlashPlayerActiveX'的子窗口。
    此方法绝对适用于中国弹弹堂官服，其他弹弹堂版本，如弹弹堂经典服、中国台湾淘米弹弹堂、越南、
    马来西亚、巴西服务器弹弹堂不保证能够识别，请根据实际情况修改代码参数。

如果你想要同时获取游戏窗口的标题文本，那么设置get_title参数为True
```python
from ddtank import get_game

hwnds, titles = get_game(get_title=True)
```
## 2.实例化角色对象 Status()
在弹弹堂中，每一个游戏窗口对应一个游戏角色。因此，每一个实例化的Status对象也对应每一个角色。
```python
from ddtank import get_game, Status

hwnds = get_game()
hwnd = hwnds[0]
my_status = Status(hwnd)
```
    如果你之前也获取了标题文本列表，那么可以在实例化Status时指定第二个参数title。

## 3.找图与找点 find()
存在以下场景：
* 获取某点的像素值(RGB)
* 判断某个(多个)点像素值是否符合条件
* 重复判断直到某个点像素符合了条件
* 获取某图片的位置

### 3.1 获取某点的像素值(RGB)
在下面的例子中，我们获取了游戏图像中(200, 200)处的像素值并储存在了变量pixel中。
```python
from ddtank import get_game, Status

hwnds = get_game()
hwnd = hwnds[0]
my_status = Status(hwnd)
pixel = my_status.find('find', pos=(200, 200))
# 或者，你可以直接 find(pos=(200, 200)
```
    获取像素值使用了win32gui的GetPixel方法，而不是先截图然后访问图片数组。

### 3.2 判断某个(多个)点像素值是否符合条件
在下面的例子中，我们判断了三个点是否符合条件，如果其中某个符合了条件，
那么就会返回它的**参数名称**(例如，cdt2)。
```python
from ddtank import get_game, Status

hwnds = get_game()
hwnd = hwnds[0]
my_status = Status(hwnd)
rst = my_status.find('mfind', 
                     cdt1=((100, 100), (12, 23, 34)), 
                     cdt2=((200, 200), (34, 23, 12)), 
                     cdt3=((300, 300), (21, 32, 43)), )
```
    'mfind'也可以简写为'mf'或者'm'，取决于你的心情。
    每一种method都有许多简写方式。
### 3.3 重复判断直到某个点像素符合了条件
在下面的例子中，我们重复判断游戏图像中(200, 200)处的像素值是否为(1, 2, 3),
在实际应用中，这种情况经常适用于进入某场景前的等待。
```python
from ddtank import get_game, Status

hwnds = get_game()
hwnd = hwnds[0]
my_status = Status(hwnd)
my_status.find('rfind', pos=(200, 200), rgb=(1, 2, 3))
```
    指定method为'rfind'时，还可以设置两个参数: 'el'和'period'。
    'el'用于指定在找某点像素值不符合条件时，执行的方法。
    'period'用于指定每次循环之间的等待时间，默认为100毫秒，这是为了避免资源占用过大。
### 3.4 获取某图片的位置
用于寻找的图片储存在self.image_path内（默认值为./image），其格式必须为png。
在下面的例子中，我们有图片路径为./image/temp.png，我们在游戏图像中查找它的位置：
```python
from ddtank import get_game, Status

hwnds = get_game()
hwnd = hwnds[0]
my_status = Status(hwnd)
center_point_pos = my_status.find('find_image', img='temp')
```
返回值center_point_pos为图片的中心点位置。

    指定method为'rfind'时，还可以设置一个参数: 'part'。
    'part'用于指定寻找图片的范围。
    'part'需要传递一个元组(x, y, w, h):
    分别为左上角x坐标、左上角y坐标、宽度、高度，默认为(0, 0, 1000, 600)即整个窗口
    在有的时候，整个游戏图像中有多个相同(或高度相似)的图片，
    你可能希望仅仅在某一小片的区域内寻找图片。
   

## 4.模拟点击 click()
存在以下场景：
* 点击某处
* 某个点像素值符合条件才点击此处
* 重复判断直到某个点像素符合了条件，然后点击此处
* 获取某图片的位置，然后点击图片位置
* 重复寻找某图片，直到图片出现，然后点击图片位置


    一般来说，click方法和find方法的method及参数都是对应的。

下面的代码基本完整展示了click的使用方法。如果你学会了find的使用，那么理解click将会是顺其自然的。
```python
from ddtank import get_game, Status

hwnds = get_game()
hwnd = hwnds[0]
my_status = Status(hwnd)
my_status.click(pos=(200, 200))
my_status.click('find', pos=(200, 200), rgb=(255, 255, 255), el=lambda: print(my_status.find(pos=(200, 200))), period=1000)
my_status.click('rfind', pos=(200, 200), rgb=(255, 255, 255))
my_status.click('find_image', img='temp', part=(0, 300, 500, 300))
```

## 5.模拟按键 press()
下面的一个例子展示了press方法的使用:
```python
from ddtank import get_game, Status

hwnds = get_game()
hwnd = hwnds[0]
my_status = Status(hwnd)
key_series = ('B', 1000, 'ESC', ('M', 1000))
my_status.press(key_series)
```

    在上面的例子里，我们先模拟按下了B键，等待1秒(1000毫秒)后按下ESC键，然后持续按下M键1秒。

## 6.读取地图 read()
识别小地图，来获取各种信息。
```
风力:    {self.wind}
角度:    {self.angle}
小地图界限:    {self.map_pos}
白框位置:    {self.box_pos}
白框宽度:    {self.box_width}
蓝点:    {self.blues}
三角:    {self.cur_pos}
红点:    {self.reds}
光圈:    {self.circle}
```
    read()方法有一个参数为is_circle，默认为False，代表是否进行光圈识别。
    在副本中，我们识别当前出手的角色一般依赖三角，而在竞技中，我们依靠闪烁的光圈来定位。
    
    对于风力和角度的识别，我们使用了深度学习的方法来识别数字，如果你玩的弹弹堂版本不是官服，
    那么其识别的准确率不理想。如果你想要为你所在的服务器来训练一个独特的识别模型，你可以为我们提供数据集。

## 7.发射炮弹 shot()
不好用，以后改进。

    综合模拟发射炮弹操作
    注意，使用此方法前需要先执行self.read()方法，否则信息得不到及时更新
    :param shot_angle: 发射的角度，若传递一个元组则执行变角操作
    :param shot_strength: 发射的力度
    :param shot_item: 使用的道具按键，多个道具之间用','分隔
    :return: 无返回值
## 8.角色移动 move()

---
## 关于脚本的编写

我们建议您继承父类Status，然后重写task()方法，将脚本内容写在此方法内，
通过YourStatus.start()方法执行脚本，此方法会开辟一个子线程来执行脚本。并且，
你可以通过YourStatus.stop()方法来强制停止脚本的运行。







