Pythonで作った電卓です。  
GUIはTkinterを使用していることもあり、外部ライブラリは必要ありません。  
内部で中置記法から後置き記法(RPN)に変換しています。

曖昧な入力でもある程度受け付けてくれます。  
![calc](https://github.com/ryozitaro/calculator/assets/126104168/bfec1845-f196-4e4e-9207-4ca977e4b98d)

現時点では、パーセント数値だけを括弧で囲むと括弧無しと同じように計算しますが、GoogleやMicrosoftの電卓ではパーセント数値を小数に直すようで、RPNの処理上そこだけ違いがありますが今後同じ動作にするかは未定です。  
![スクリーンショット 2024-07-09 213655](https://github.com/ryozitaro/calculator/assets/126104168/ee64dd34-ac59-4dbe-b3b2-b6ed079633a2)
