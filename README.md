# Droplets Simulation
Simulation of Virus-Laden Droplets Behavior in AFDET

## 現在移行期間

## フォルダ構成
とりあえず[ここ](https://qiita.com/flcn-x/items/c866eec8824a3cd70fa8#%E6%9C%80%E5%BE%8C%E3%81%AB)
をまねる。

## 使い方
  つかえません。

## 条件ファイル(setting.yaml)解説
  現在工事中
  ### condition.nml
  - **リスタート位置 num_restart**
    - 通常は`0`を指定
    - `1以上`にすると、その値に対応するbackupファイルが読み込まれ、そこからリスタートが始まる
  - **初期分布ファイル名 initialDistributionFName**
    - 指定したbackupファイル(.bu)が読み込まれ、それを飛沫初期分布とする
    - 初期分布を固定したくない場合はコメントアウトすること
  - **飛沫周期発生 periodicGeneration**
    - 1秒当たりの発生飛沫数（整数）を指定
    - 初期配置飛沫をすべてNonActiveにしたのち、順次Activateしていくので、初期配置数が飛沫数の上限となる
  - **気流データファイル名 path2FlowFile**
    - 実行ディレクトリからの相対パス、もしくは絶対パスを指定
    - 現在可能な流れ場ファイル：
      - VTK
      - INP
      - FLD
    - CUBE格子(PLOT3D)は、予め非構造格子に変換してから計算してください。
    - .arrayファイルを指定する場合、別途メッシュファイルが必要なので、`meshFile = ***`と指定する
  - **ステップ数オフセット OFFSET**
    - 飛沫計算を、流体連番ファイルの途中の番号から始めたいときに指定
  - **気流データを周期的に用いる場合の先頭と末尾 LoopHead, LoopTail**
    - 任意の区間の流体連番ファイルを繰り返し用いるときに指定（例えば呼吸のサイクル）
    - `(先頭) = (末尾)` とすると、そのステップ数到達後は流れ場の更新が起こらなくなる
    - `(先頭) > (末尾)` とすれば、特殊な処理は起こらず、流体連番ファイルが順番に読み込まれる
  ### initial_position.csv
  - 初期飛沫の配置帯（直方体）を設定する
  - 左から順に、直方体の中心座標(x,y,z), 直方体の幅(x,y,z)
  - 改行すれば配置帯を複数設定できる


## 方程式

  ### 飛沫の蒸発方程式

  $$ \frac{dr}{dt} \space = \space -\left(1-\frac{RH}{100}\right) \cdot \frac{D e_{s}(T)}{\rho_{w} R_{v} T} \cdot \frac{1}{r} $$
  
  プログラム内では、２次精度ルンゲクッタ法で解いている。
  
  ### 飛沫の運動方程式

$$ m \frac{d \mathbf{v}}{dt} \space = \space m \mathbf{g} \space + \space C_D (\mathbf{v}) \space \cdot \space \frac{1}{2} \rho_a S \left | \mathbf{u}_a - \mathbf{v} \right | (\mathbf{u}_a - \mathbf{v}) $$

  プログラム内では、上式を無次元化・離散化した次式を解いている。
    
$$ \bar{\mathbf{v}}^{n + 1} \space = \space \frac{\bar{\mathbf{v}}^{n} \space + \space (\bar{\mathbf{g}} \space + \space C \bar{\mathbf{u}}_a)\Delta \bar{t}}{1 \space + \space C\Delta \bar{t}} \quad \left ( C \space = \space \frac{3 \rho_a}{8 \rho_w} \frac{C_D ( \mathbf{v}^{n} ) \left | \bar{\mathbf{u}}_a - \bar{\mathbf{v}}^{n} \right |}{\bar{r}^{n+1}} \right ) $$

## サブプログラム
  現在工事中
