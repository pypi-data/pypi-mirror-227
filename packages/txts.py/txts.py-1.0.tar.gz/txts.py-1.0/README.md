# :newspaper: txts.py
*Python wrapper for interacting with [txts](https://https://github.com/txts-team/txts)*
## :hammer_and_wrench: Contributing

This project is very much work in progress, any contributions would be appreciated<br>
If you make a pull request please use proper labels and follow the contributor [Code Of Conduct](https://github.com/txts-team/txts.py/blob/master/CODE_OF_CONDUCT.md)

## :arrow_down: Installing

```
python3 -m pip install -U txts.py
```

## :bulb: Simple Example

```python
import txts

instance = txts.TxtInstance('instance_url')
print(instance.Status())
try:
    instance.EditPage('username','secret','content')
    print('Sucessfully updated page!')
except:
    print('Failed to update page!')
```    

## :link: Links

[Txts Discord](https://discord.gg/Y5QfmF9uW3) :headphones: <br>
[Txts official instance](https://txts.sudokoko.xyz/) :globe_with_meridians:
