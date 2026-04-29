#!/usr/bin/env python3
"""
TOEFL3800.csv 裏面カラム変換スクリプト

変換方針:
  - 【＠】【変化】【分節】等の辞書形式ノイズを除去
  - 主要な意味（1〜2個）と例文（1〜2個）を抽出・整形
  - マークアップなし・例文なしのシンプルエントリには例文を付与

出力: TOEFL3800_clean.csv
"""

import csv
import re
from pathlib import Path

INPUT = Path(__file__).parent / "TOEFL3800.csv"
OUTPUT = Path(__file__).parent / "TOEFL3800_clean.csv"

# ---------------------------------------------------------------------------
# シンプルエントリ用辞書
# (word) -> (clean_meaning, "English example（日本語訳）")
# ---------------------------------------------------------------------------
SIMPLE_EXAMPLES: dict[str, tuple[str, str]] = {
    "observatory": (
        "観測所；天文台",
        "The Mauna Kea Observatory offers astronomers a clear view of the night sky."
        "（マウナケア天文台は天文学者に澄んだ夜空を見渡す場を与える）",
    ),
    "herbivore": (
        "草食動物",
        "Deer are herbivores that feed mainly on grass and leaves."
        "（鹿は主に草や葉を食べる草食動物だ）",
    ),
    "lava": (
        "溶岩",
        "Hot lava flowed down the slope during the volcanic eruption."
        "（噴火中、熱い溶岩が斜面を流れ下った）",
    ),
    "larva": (
        "幼虫",
        "The caterpillar is the larva of a butterfly.（毛虫はチョウの幼虫だ）",
    ),
    "fireplace": (
        "暖炉",
        "We sat by the fireplace to keep warm on the cold night."
        "（寒い夜、私たちは暖炉のそばで暖を取った）",
    ),
    "carve": (
        "彫る；刻む",
        "He carved his initials into the tree bark."
        "（彼は木の皮に自分のイニシャルを刻んだ）",
    ),
    "exclaim": (
        "（驚き・喜びなどで）叫ぶ",
        "She exclaimed in surprise when she saw the gift."
        "（贈り物を見て彼女は驚いて声をあげた）",
    ),
    "herb": (
        "ハーブ；薬草",
        "Basil is an herb commonly used in Italian cooking."
        "（バジルはイタリア料理でよく使われるハーブだ）",
    ),
    "accomplish": (
        "成し遂げる；達成する",
        "She accomplished all her goals before turning 30."
        "（彼女は30歳になる前にすべての目標を達成した）",
    ),
    "carbon": (
        "炭素",
        "Carbon dioxide is released when fossil fuels are burned."
        "（化石燃料が燃焼すると二酸化炭素が放出される）",
    ),
    "cheerfully": (
        "にこやかに；快活に",
        "She greeted everyone cheerfully every morning."
        "（彼女は毎朝みんなをにこやかに迎えた）",
    ),
    "saw": (
        "のこぎり",
        "He used a saw to cut the plank in half.（彼はのこぎりで板を半分に切った）",
    ),
    "sew": (
        "縫う",
        "She sewed the button back onto the shirt."
        "（彼女はシャツにボタンを縫い付け直した）",
    ),
    "parcel": (
        "小包",
        "She received a parcel from her sister in the mail."
        "（彼女は姉から郵便で小包を受け取った）",
    ),
    "navy": (
        "海軍",
        "He served in the navy for twenty years.（彼は20年間海軍に勤務した）",
    ),
    "odor": (
        "臭い；においl",
        "The odor from the garbage was unbearable.（ゴミの臭いは耐えられなかった）",
    ),
    "brochure": (
        "パンフレット；小冊子",
        "The travel agency sent me a brochure about Hawaii."
        "（旅行会社がハワイのパンフレットを送ってきた）",
    ),
    "tuition": (
        "授業料",
        "University tuition has risen sharply over the past decade."
        "（大学の授業料は過去10年で急激に上昇した）",
    ),
    "sculpture": (
        "彫刻（作品）",
        "The museum has an impressive collection of ancient sculptures."
        "（その美術館には古代彫刻の印象的なコレクションがある）",
    ),
    "habitat": (
        "生息地",
        "Deforestation destroys the natural habitat of many animals."
        "（森林破壊は多くの動物の自然の生息地を壊す）",
    ),
    "resist": (
        "抵抗する；こらえる",
        "She could not resist the temptation to eat the cake."
        "（彼女はケーキを食べたいという誘惑に抵抗できなかった）",
    ),
    "excuse": (
        "（動）言い訳する；免除する ／（名）言い訳",
        "He always makes excuses for being late.（彼はいつも遅刻の言い訳をする）",
    ),
    "restrict": (
        "制限する；限定する",
        "Access to the building is restricted to authorized personnel."
        "（建物への立入りは許可された職員のみに制限されている）",
    ),
    "divide": (
        "分ける；割る",
        "The teacher divided the class into groups of four."
        "（先生はクラスを4人のグループに分けた）",
    ),
    "priest": (
        "聖職者；神父",
        "The priest delivered a sermon on forgiveness."
        "（神父は赦しについての説教を行った）",
    ),
    "resume": (
        "再開する",
        "Classes will resume after the holiday break.（休暇後、授業が再開される）",
    ),
    "maize": (
        "トウモロコシ",
        "Maize was first cultivated in Mexico thousands of years ago."
        "（トウモロコシは数千年前にメキシコで最初に栽培された）",
    ),
    "brave": (
        "勇敢な",
        "It was brave of him to speak up against the injustice."
        "（不正に立ち向かったのは勇気ある行動だった）",
    ),
    "gene": (
        "遺伝子",
        "Eye color is determined by genes inherited from one's parents."
        "（目の色は親から受け継いだ遺伝子によって決まる）",
    ),
    "wrap": (
        "包む；巻く",
        "She wrapped the gift in colorful paper.（彼女はギフトをカラフルな紙で包んだ）",
    ),
    "airflow": (
        "気流；空気の流れ",
        "Proper airflow is essential for engine cooling."
        "（適切な空気の流れはエンジン冷却に不可欠だ）",
    ),
    "humble": (
        "謙虚な；粗末な",
        "Despite his success, he remained humble and approachable."
        "（成功しても彼は謙虚で親しみやすかった）",
    ),
    "modest": (
        "謙虚な；控えめな",
        "She was modest about her achievements."
        "（彼女は自分の業績について控えめだった）",
    ),
    "waterproof": (
        "防水の",
        "This jacket is waterproof, so you won't get wet in the rain."
        "（このジャケットは防水なので雨でも濡れない）",
    ),
    "orbit": (
        "軌道；公転する",
        "The Earth takes one year to complete its orbit around the Sun."
        "（地球が太陽の軌道を一周するのに1年かかる）",
    ),
    "shallow": (
        "浅い；表面的な",
        "The river is too shallow to swim in at this point."
        "（この地点では川が浅すぎて泳げない）",
    ),
    "secure": (
        "安全な；安定した；確保する",
        "Make sure all your passwords are secure."
        "（すべてのパスワードを安全に保つようにしてください）",
    ),
    "garment": (
        "衣服；衣類",
        "The garment factory employs hundreds of workers."
        "（その衣服工場は何百人もの労働者を雇っている）",
    ),
    "tribe": (
        "部族；種族",
        "The tribe lived in harmony with nature for centuries."
        "（その部族は何世紀もの間、自然と調和して生きてきた）",
    ),
    "faithful": (
        "忠実な；誠実な",
        "The dog was faithful to its owner until the very end."
        "（その犬は最後まで飼い主に忠実だった）",
    ),
    "load": (
        "積荷；負担；積む",
        "The truck was carrying a heavy load of timber."
        "（トラックは重い木材の積荷を運んでいた）",
    ),
    "rhythm": (
        "リズム；律動",
        "She danced to the rhythm of the drums."
        "（彼女はドラムのリズムに合わせて踊った）",
    ),
    "atlas": (
        "地図帳",
        "He consulted the atlas to plan his road trip."
        "（ドライブ旅行を計画するために地図帳を調べた）",
    ),
    "fragment": (
        "破片；断片",
        "Fragments of ancient pottery were found at the excavation site."
        "（発掘現場で古代陶器の破片が見つかった）",
    ),
    "marsh": (
        "湿地；沼",
        "Many birds nest in the marsh during spring.（多くの鳥が春に湿地で巣を作る）",
    ),
    "vary": (
        "異なる；変わる",
        "Prices vary depending on the season.（価格は季節によって変わる）",
    ),
    "nebula": (
        "星雲",
        "The Orion Nebula is one of the brightest nebulae in the night sky."
        "（オリオン星雲は夜空で最も明るい星雲の一つだ）",
    ),
    "algae": (
        "藻類",
        "Algae are simple organisms that grow in water and produce oxygen."
        "（藻類は水中で育ち酸素を生み出す単純な生物だ）",
    ),
    "civic": (
        "市民の；公民の",
        "Voting is a civic duty in a democracy.（投票は民主主義における市民の義務だ）",
    ),
    "tragedy": (
        "悲劇",
        "The sinking of the Titanic was one of history's greatest tragedies."
        "（タイタニックの沈没は歴史上最大の悲劇の一つだ）",
    ),
    "guess": (
        "推測する；当てる",
        "I couldn't figure out the answer, so I just guessed."
        "（答えが分からなかったので、ただ推測した）",
    ),
    "primitive": (
        "原始的な；未開の",
        "Primitive tools were made from stone and bone."
        "（原始的な道具は石と骨から作られた）",
    ),
    "awful": (
        "ひどい；恐ろしい",
        "The storm caused awful damage to the coastal town."
        "（嵐は沿岸の町にひどい被害をもたらした）",
    ),
    "plant": (
        "植物；工場（施設）",
        "The automobile plant employs 5,000 workers."
        "（その自動車工場は5,000人の従業員を雇っている）",
    ),
    "stable": (
        "安定した；馬小屋",
        "The patient's condition is now stable.（患者の容体は現在安定している）",
    ),
    "toe": (
        "つまさき",
        "She stubbed her toe on the corner of the table."
        "（彼女はテーブルの角につまさきをぶつけた）",
    ),
    "flag": (
        "旗；〔勢いが〕衰える",
        "His enthusiasm began to flag after hours of tedious work."
        "（単調な作業が何時間も続き、彼の熱意が衰え始めた）",
    ),
    "hostage": (
        "人質",
        "The terrorists held three people hostage for two days."
        "（テロリストは3人を2日間人質にした）",
    ),
    "motif": (
        "主題；モチーフ",
        "A recurring motif in his novels is the struggle for identity."
        "（彼の小説の繰り返すモチーフはアイデンティティをめぐる葛藤だ）",
    ),
    "beehive": (
        "ハチの巣",
        "The beehive in the garden contains thousands of bees."
        "（庭のハチの巣には何千匹ものミツバチが住んでいる）",
    ),
    "harbor": (
        "港；かくまう",
        "The ship sailed into the harbor at dawn.（船は夜明けに港へ入った）",
    ),
    "shave": (
        "（ひげ・毛を）そる",
        "He shaves his beard every morning before going to work."
        "（彼は毎朝出勤前にひげをそる）",
    ),
    "spectacle": (
        "光景；見せ物",
        "The fireworks display was quite a spectacle.（花火の演技は見事な光景だった）",
    ),
    "evaluate": (
        "評価する；査定する",
        "The teacher carefully evaluated each student's performance."
        "（教師は生徒一人ひとりの成績を丁寧に評価した）",
    ),
    "exception": (
        "例外",
        "There are no exceptions to this rule.（この規則には例外がない）",
    ),
    "obtain": (
        "手に入れる；獲得する",
        "She obtained a scholarship to study abroad."
        "（彼女は留学のための奨学金を獲得した）",
    ),
    "glory": (
        "栄光；光栄",
        "The team basked in the glory of their championship victory."
        "（チームは優勝の栄光に浸った）",
    ),
    "primate": ("霊長類", "Apes and monkeys are primates.（類人猿とサルは霊長類だ）"),
    "property": (
        "財産；特性",
        "Water has the property of expanding when it freezes."
        "（水は凍ると膨張する特性がある）",
    ),
    "deficit": (
        "赤字；不足",
        "The government is running a large budget deficit."
        "（政府は大きな財政赤字を抱えている）",
    ),
    "throat": (
        "喉",
        "She had a sore throat and couldn't sing.（彼女は喉が痛くて歌えなかった）",
    ),
    "artifact": (
        "人工遺物；工芸品",
        "Archaeologists discovered ancient artifacts at the site."
        "（考古学者たちが遺跡で古代の遺物を発見した）",
    ),
    "plural": (
        "複数（形）の",
        "The plural of 'child' is 'children'.（childの複数形はchildrenだ）",
    ),
    "flour": (
        "小麦粉",
        "Add two cups of flour to the batter and mix well."
        "（生地に小麦粉を2カップ加えてよく混ぜる）",
    ),
    "ingredient": (
        "材料；成分",
        "Fresh ingredients are essential for good cooking."
        "（新鮮な材料は良い料理に欠かせない）",
    ),
    "stellar": (
        "星の；卓越した",
        "The scientist studied stellar formation in distant galaxies."
        "（科学者は遠い銀河の星形成を研究した）",
    ),
    "stride": (
        "大股で歩く；歩幅",
        "He strode confidently across the stage.（彼は自信を持って舞台を大股で歩いた）",
    ),
    "seaport": (
        "海港",
        "Rotterdam is one of Europe's busiest seaports."
        "（ロッテルダムはヨーロッパで最も忙しい海港の一つだ）",
    ),
    "infection": (
        "感染；伝染",
        "Wash your hands frequently to prevent infection."
        "（感染を防ぐために頻繁に手を洗ってください）",
    ),
    "sue": (
        "告訴する；訴える",
        "She sued the company for workplace discrimination."
        "（彼女は職場差別で会社を訴えた）",
    ),
    "spear": (
        "やり；槍",
        "Early hunters used spears to catch large animals."
        "（初期の狩猟者は槍を使って大型動物を捕まえた）",
    ),
    "spontaneous": (
        "自発的な；自然発生的な",
        "The crowd broke into spontaneous applause at the end of the speech."
        "（演説の終わりに観衆が自然に拍手した）",
    ),
    "hospitality": (
        "もてなし；歓待",
        "The hotel was renowned for its warm hospitality."
        "（そのホテルは温かいもてなしで有名だった）",
    ),
    "seashore": (
        "海岸",
        "Children love playing on the seashore in summer."
        "（子供たちは夏に海岸で遊ぶのが大好きだ）",
    ),
    "bathe": (
        "入浴する；洗う",
        "The doctor advised her to bathe the wound gently twice a day."
        "（医師は傷口を1日2回優しく洗うよう指示した）",
    ),
    "wake": (
        "目覚める；航跡",
        "He woke up early to catch the morning flight."
        "（彼は朝の便に乗るために早く起きた）",
    ),
    "harsh": (
        "厳しい；過酷な",
        "The harsh desert climate made survival very difficult."
        "（過酷な砂漠の気候は生存を非常に困難にした）",
    ),
    "privilege": (
        "特権；恩典",
        "Education is a privilege that not everyone has access to."
        "（教育はすべての人が得られるわけではない特権だ）",
    ),
    "plentiful": (
        "豊富な；たくさんの",
        "Food was plentiful during the harvest season."
        "（収穫の季節には食べ物が豊富だった）",
    ),
    "abundant": (
        "豊富な；十分な",
        "The region has abundant natural resources."
        "（その地域には豊富な天然資源がある）",
    ),
    "reliable": (
        "信頼できる；頼りになる",
        "She is a reliable worker who always meets her deadlines."
        "（彼女は常に締め切りを守る信頼できる社員だ）",
    ),
    "appetite": (
        "食欲；欲求",
        "Exercise can increase your appetite.（運動は食欲を増進させることがある）",
    ),
    "funeral": (
        "葬式；告別式",
        "The whole village attended the funeral.（村全体が葬式に参列した）",
    ),
    "genuine": (
        "本物の；誠実な",
        "The museum confirmed the painting was a genuine Picasso."
        "（美術館はその絵が本物のピカソだと確認した）",
    ),
    "shore": (
        "岸；海岸",
        "The sailors were relieved to see the shore after weeks at sea."
        "（何週間も海上にいた後、船乗りたちは岸が見えてほっとした）",
    ),
    "vaccine": (
        "ワクチン",
        "The flu vaccine is recommended every year for the elderly."
        "（インフルエンザワクチンは高齢者に毎年接種が推奨されている）",
    ),
    "serve": (
        "奉仕する；役立つ；給仕する",
        "She served in the Peace Corps for two years.（彼女は2年間平和部隊で奉仕した）",
    ),
    "narrowly": (
        "かろうじて；辛うじて",
        "The driver narrowly escaped the accident.（運転手は事故をかろうじて免れた）",
    ),
    "nursery": (
        "苗床；保育室",
        "The plants were grown in the nursery before being transplanted outdoors."
        "（植物は屋外に移植される前に苗床で育てられた）",
    ),
    "credible": (
        "信頼できる；信憑性のある",
        "The witness gave a credible account of the events."
        "（目撃者は出来事について信頼できる説明をした）",
    ),
    "abdomen": (
        "腹部",
        "The doctor examined the patient's abdomen for signs of pain."
        "（医師は痛みの兆候がないか患者の腹部を診察した）",
    ),
    "prosperity": (
        "繁栄；成功",
        "The country enjoyed a long period of economic prosperity."
        "（その国は長い経済的繁栄の時期を享受した）",
    ),
    "Pacific Ocean": (
        "太平洋",
        "The Pacific Ocean is the largest and deepest ocean on Earth."
        "（太平洋は地球上で最大かつ最深の海洋だ）",
    ),
    "tailor": (
        "仕立て屋；（合わせて）調整する",
        "The tailor altered the suit to fit him perfectly."
        "（仕立て屋はスーツを彼にぴったり合うように直した）",
    ),
    "discriminate": (
        "差別する；識別する",
        "It is illegal to discriminate against employees based on race."
        "（人種に基づいて従業員を差別することは違法だ）",
    ),
    "assume": (
        "仮定する；思い込む",
        "Don't assume everyone agrees with you."
        "（みんなが同意していると思い込まないで）",
    ),
    "considerable": (
        "かなりの；相当の",
        "The project required a considerable amount of time and effort."
        "（そのプロジェクトにはかなりの時間と労力が必要だった）",
    ),
    "currency": (
        "通貨",
        "The euro is the official currency of many European countries."
        "（ユーロは多くのヨーロッパ諸国の公式通貨だ）",
    ),
    "intend": (
        "意図する；〜するつもりである",
        "I intend to finish the report by Friday."
        "（金曜日までにレポートを終わらせるつもりだ）",
    ),
    "dwelling": (
        "住居；住まい",
        "The ancient dwellings were carved into the cliffs."
        "（古代の住居は崖に掘られたものだった）",
    ),
    "qualification": (
        "資格；要件",
        "A degree in engineering is the minimum qualification for this position."
        "（この職の最低資格は工学の学位だ）",
    ),
    "Supreme Court": (
        "最高裁判所",
        "The Supreme Court ruled in favor of the defendant."
        "（最高裁判所は被告に有利な判決を下した）",
    ),
    "nomad": (
        "遊牧民；放浪者",
        "Nomads move from place to place in search of food and water."
        "（遊牧民は食料と水を求めて場所から場所へ移動する）",
    ),
    "gland": (
        "腺（せん）",
        "The thyroid gland regulates the body's metabolism."
        "（甲状腺は体の代謝を調節する）",
    ),
    "mercury": (
        "水銀；水星",
        "Mercury is a toxic liquid metal formerly used in thermometers."
        "（水銀はかつて温度計に使われていた有毒な液体金属だ）",
    ),
    "distinctive": (
        "特有の；際立った",
        "Each bird species has a distinctive call."
        "（鳥の各種は特有の鳴き声を持っている）",
    ),
    "diligent": (
        "勤勉な；まじめな",
        "Her diligent study habits earned her top grades."
        "（勤勉な学習習慣が彼女に最高の成績をもたらした）",
    ),
    "substantial": (
        "相当な；実質的な",
        "There is a substantial difference between the two proposals."
        "（二つの提案の間には相当な違いがある）",
    ),
    "wrist": (
        "手首",
        "She broke her wrist in a fall on the ice."
        "（彼女は氷の上で転んで手首を骨折した）",
    ),
    "swamp": (
        "沼地；（仕事などで）圧倒する",
        "The explorers struggled to cross the dense swamp."
        "（探検家たちは深い沼地を渡るのに苦労した）",
    ),
    "hydrogen": (
        "水素",
        "Water is made up of two hydrogen atoms and one oxygen atom."
        "（水は2つの水素原子と1つの酸素原子でできている）",
    ),
    "account": (
        "口座；説明；みなす",
        "I opened a savings account at the bank last week."
        "（先週、銀行に普通預金口座を開設した）",
    ),
    "arithmetic": (
        "算数；四則計算",
        "Basic arithmetic is essential for everyday life."
        "（基本的な算数は日常生活に欠かせない）",
    ),
    "meteor": (
        "流星；隕石",
        "We saw a bright meteor streak across the night sky."
        "（夜空を明るい流星が横切るのを見た）",
    ),
    "ceramic": (
        "陶磁器；セラミック",
        "The museum has an excellent collection of Japanese ceramic art."
        "（その美術館は優れた日本の陶芸コレクションを持っている）",
    ),
    "fluid": (
        "流体；液体；流動的な",
        "Drink plenty of fluids when you have a fever."
        "（熱があるときはたくさん水分を摂って）",
    ),
    "blowhole": (
        "（クジラなどの）噴気孔",
        "The whale surfaced and breathed through its blowhole."
        "（クジラが水面に出て噴気孔から呼吸した）",
    ),
    "grief": (
        "深い悲しみ；悲嘆",
        "She was overcome with grief at the loss of her husband."
        "（夫を失い、彼女は悲しみに打ちひしがれた）",
    ),
    "copper": (
        "銅",
        "Copper is an excellent conductor of electricity.（銅は電気の優れた導体だ）",
    ),
    "seasoning": (
        "調味料；スパイス",
        "Add seasoning to taste before serving."
        "（食卓に出す前にお好みで調味料を加えてください）",
    ),
    "reptile": (
        "爬虫類",
        "Snakes, lizards, and turtles are all reptiles."
        "（ヘビ、トカゲ、カメはすべて爬虫類だ）",
    ),
    "Tropical Zone": (
        "熱帯",
        "The tropical zone receives the most solar radiation throughout the year."
        "（熱帯は年間を通じて最も多くの太陽放射を受ける）",
    ),
    "tin": (
        "スズ；缶",
        "Tin is used to coat steel cans to prevent rusting."
        "（スズはサビを防ぐためにスチール缶のコーティングに使われる）",
    ),
    "staple": (
        "主要な；基本的な；主食（品）",
        "Rice is a staple food in many Asian countries."
        "（米はアジア多くの国々の主食だ）",
    ),
    "treasury": (
        "財務省；宝庫",
        "The Treasury Department manages the government's finances."
        "（財務省は政府の財務を管理する）",
    ),
    "tree sap": (
        "樹液",
        "Maple syrup is made from the sap of maple trees."
        "（メープルシロップはカエデの樹液から作られる）",
    ),
    "algebra": (
        "代数（学）",
        "Algebra uses symbols and letters to represent numbers and solve equations."
        "（代数は記号と文字を使って数を表し方程式を解く）",
    ),
    "scenery": (
        "風景；景色",
        "The mountain scenery was absolutely breathtaking."
        "（山の景色は息をのむほど美しかった）",
    ),
    "frost": (
        "霜；霜が降りる",
        "There was a heavy frost on the ground this morning."
        "（今朝は地面に厚い霜が降りていた）",
    ),
    "Arctic": (
        "北極（の）",
        "The Arctic ice cap is melting rapidly due to climate change."
        "（北極の氷は気候変動により急速に溶けている）",
    ),
    "sulfur": (
        "硫黄",
        "Sulfur dioxide released by volcanoes can cause acid rain."
        "（火山から放出される二酸化硫黄は酸性雨を引き起こすことがある）",
    ),
    "globe": (
        "地球；地球儀；球体",
        "He spun the globe and pointed to Brazil."
        "（彼は地球儀を回してブラジルを指差した）",
    ),
    "squash": (
        "押しつぶす；ウリ科の野菜",
        "She squashed the spider with her shoe.（彼女は靴でクモを踏みつぶした）",
    ),
    "neat": (
        "きちんとした；こぎれいな",
        "His desk was always neat and well organized."
        "（彼の机はいつも整然と整理されていた）",
    ),
    "germ": (
        "細菌；病原菌",
        "Wash your hands thoroughly to prevent the spread of germs."
        "（細菌の拡散を防ぐために手をしっかり洗ってください）",
    ),
    "desire": (
        "欲求；望む",
        "She desired nothing more than peace and a quiet life."
        "（彼女は平和と静かな生活以上のものを望まなかった）",
    ),
    "genre": (
        "ジャンル；様式",
        "Mystery is my favorite literary genre."
        "（ミステリーは私の一番好きな文学ジャンルだ）",
    ),
    "indicate": (
        "示す；指し示す",
        "The arrow indicates the direction of the emergency exit."
        "（矢印は非常口の方向を示している）",
    ),
    "reluctant": (
        "気が進まない；嫌々ながらの",
        "She was reluctant to speak in front of a large audience."
        "（彼女は大勢の聴衆の前で話すことを嫌がっていた）",
    ),
    "sprout": (
        "芽；発芽する",
        "The seeds began to sprout after just three days.（種は3日で芽を出し始めた）",
    ),
    "allergic": (
        "アレルギーの",
        "She is allergic to peanuts and must avoid them entirely."
        "（彼女はピーナッツアレルギーで完全に避けなければならない）",
    ),
    "coal": (
        "石炭",
        "Coal was the primary energy source during the Industrial Revolution."
        "（石炭は産業革命時代の主要なエネルギー源だった）",
    ),
    "generous": (
        "気前のよい；寛大な",
        "It was very generous of him to donate to the charity."
        "（慈善団体に寄付するとは彼はとても気前がよかった）",
    ),
    "interpret": (
        "通訳する；解釈する",
        "She interpreted for the visiting foreign delegation."
        "（彼女は訪問中の外国代表団のために通訳した）",
    ),
    "faculty": (
        "学部；教授陣；能力",
        "The faculty voted to revise the curriculum."
        "（教授陣はカリキュラムの改訂に投票した）",
    ),
    "dawn": (
        "夜明け；始まり",
        "They set out at dawn to begin the long journey."
        "（彼らは長い旅を始めるために夜明けに出発した）",
    ),
    "eloquent": (
        "雄弁な；説得力のある",
        "The lawyer made an eloquent argument before the jury."
        "（弁護士は陪審員の前で説得力ある弁論を行った）",
    ),
    "enact": (
        "制定する；立法化する",
        "Congress enacted a new law to protect consumer rights."
        "（議会は消費者の権利を守る新しい法律を制定した）",
    ),
    "facility": (
        "施設；設備",
        "The sports facility has a swimming pool and a gym."
        "（そのスポーツ施設にはプールとジムがある）",
    ),
    "herd": (
        "（牛・羊などの）群れ；追いやる",
        "A herd of cattle grazed on the hillside."
        "（牛の群れが丘の斜面で草を食んでいた）",
    ),
    "universe": (
        "宇宙；（全）世界",
        "Scientists estimate the universe is about 13.8 billion years old."
        "（科学者たちは宇宙が約138億年前から存在していると推定している）",
    ),
    "spectator": (
        "観客；見物人",
        "Thousands of spectators gathered to watch the final match."
        "（何千人もの観客が決勝戦を観戦するために集まった）",
    ),
    "invitation": (
        "招待（状）",
        "She accepted the invitation to attend the wedding ceremony."
        "（彼女は結婚式への招待を承諾した）",
    ),
    "synonym": (
        "同義語；類義語",
        "Happy and joyful are synonyms with slightly different nuances."
        "（happyとjoyfulは若干ニュアンスの違う同義語だ）",
    ),
    "molecule": (
        "分子",
        "A water molecule consists of two hydrogen atoms and one oxygen atom."
        "（水分子は2つの水素原子と1つの酸素原子でできている）",
    ),
    "Antarctic": (
        "南極（の）",
        "Scientists have found evidence of climate change in the Antarctic."
        "（科学者たちは南極で気候変動の証拠を発見した）",
    ),
    "nerve": (
        "神経；度胸",
        "The accident damaged the nerve in his hand.（事故で彼の手の神経が損傷した）",
    ),
    "bury": (
        "埋める；埋葬する",
        "He buried the treasure in his backyard.（彼は裏庭に宝を埋めた）",
    ),
    "Stone Age": (
        "石器時代",
        "Stone Age tools made of flint have been found across Europe."
        "（ヨーロッパ各地で石器時代の火打石製の道具が見つかっている）",
    ),
    "mark": (
        "印をつける；記録する",
        "The teacher marked the attendance at the start of each class."
        "（教師は授業の始めに出席を記録した）",
    ),
    "solar system": (
        "太陽系",
        "There are eight planets in our solar system."
        "（私たちの太陽系には8つの惑星がある）",
    ),
    "cobblestone street": (
        "石畳の通り",
        "The old town was full of charming cobblestone streets."
        "（旧市街は魅力的な石畳の道であふれていた）",
    ),
    "polar bear": (
        "ホッキョクグマ；シロクマ",
        "Polar bears depend on sea ice to hunt seals."
        "（ホッキョクグマはアザラシを狩るために海氷に依存している）",
    ),
    "natural science": (
        "自然科学",
        "Physics, chemistry, and biology are all branches of natural science."
        "（物理、化学、生物はすべて自然科学の分野だ）",
    ),
    "chronological order": (
        "年代順",
        "Please list the historical events in chronological order."
        "（歴史的出来事を年代順に列挙してください）",
    ),
    "sea anemone": (
        "イソギンチャク",
        "Clownfish live among the tentacles of sea anemones for protection."
        "（クマノミは身を守るためにイソギンチャクの触手の中に住んでいる）",
    ),
    "paddy field": (
        "水田",
        "The paddy fields are flooded with water during the rice-growing season."
        "（水田は稲作の季節に水で満たされる）",
    ),
    "double helix": (
        "二重らせん",
        "Watson and Crick discovered the double helix structure of DNA in 1953."
        "（ワトソンとクリックは1953年にDNAの二重らせん構造を発見した）",
    ),
    "electron microscope": (
        "電子顕微鏡",
        "Viruses are too small to see without an electron microscope."
        "（ウイルスは電子顕微鏡なしには見えないほど小さい）",
    ),
    "coniferous tree": (
        "針葉樹",
        "Pine and spruce are common coniferous trees in northern forests."
        "（松とトウヒは北方の森でよく見られる針葉樹だ）",
    ),
    "latency period": (
        "潜伏期",
        "The virus has a latency period of several days before symptoms appear."
        "（そのウイルスは症状が現れる前に数日間の潜伏期がある）",
    ),
    "purchasing power": (
        "購買力",
        "Inflation erodes the purchasing power of consumers."
        "（インフレは消費者の購買力を蝕む）",
    ),
    "right angle": (
        "直角",
        "A square has four right angles of 90 degrees each."
        "（正方形はそれぞれ90度の直角が4つある）",
    ),
    "reclaimed land": (
        "埋立地；開拓地",
        "The airport was built on reclaimed land near the coast."
        "（その空港は海岸近くの埋立地に建設された）",
    ),
    "mating season": (
        "交尾期；繁殖期",
        "Male deer compete fiercely for mates during the mating season."
        "（雄鹿は繁殖期にメスをめぐって激しく争う）",
    ),
    "motor neuron": (
        "運動ニューロン",
        "Motor neurons transmit signals from the brain to the muscles."
        "（運動ニューロンは脳から筋肉へ信号を伝達する）",
    ),
    "sense organ": (
        "感覚器官",
        "The eyes, ears, and nose are all sense organs."
        "（目、耳、鼻はすべて感覚器官だ）",
    ),
    "vocal cords": (
        "声帯",
        "Singers must take good care of their vocal cords."
        "（歌手は声帯を大切にしなければならない）",
    ),
    "public hygiene": (
        "公衆衛生",
        "Improvements in public hygiene have greatly increased life expectancy."
        "（公衆衛生の改善が平均寿命を大幅に延ばした）",
    ),
    "microscopic organism": (
        "微生物",
        "Microscopic organisms in the soil break down organic matter."
        "（土壌の微生物は有機物を分解する）",
    ),
    "mural painting": (
        "壁画",
        "The mural painting covered the entire interior wall of the cathedral."
        "（壁画は大聖堂の室内壁全体を覆っていた）",
    ),
    "unaided eye": (
        "肉眼",
        "Stars are visible to the unaided eye on a clear, dark night."
        "（晴れた暗い夜には星は肉眼で見える）",
    ),
    "deciduous tree": (
        "落葉樹",
        "Maple and oak are deciduous trees that shed their leaves in autumn."
        "（カエデとオークは秋に葉を落とす落葉樹だ）",
    ),
    "reproductive organ": (
        "生殖器官",
        "Flowers are the reproductive organs of flowering plants."
        "（花は顕花植物の生殖器官だ）",
    ),
    "arrow tip": (
        "矢じり",
        "Stone arrow tips were widely used by prehistoric hunters."
        "（石の矢じりは先史時代の狩猟者に広く使われた）",
    ),
    "venomous snake": (
        "毒蛇",
        "The cobra is one of the most venomous snakes in the world."
        "（コブラは世界で最も毒性の強い毒蛇の一つだ）",
    ),
    "compound eye": (
        "複眼",
        "Insects have compound eyes that provide a wide field of vision."
        "（昆虫は広い視野を持つ複眼を持っている）",
    ),
    "fraternal society": (
        "友愛団体；共済組合",
        "He joined a fraternal society that supported veterans and their families."
        "（彼は退役軍人とその家族を支援する友愛団体に加入した）",
    ),
    "mixed breed": (
        "雑種；混血",
        "Mixed breed dogs are often known for their good health and temperament."
        "（雑種犬は健康と気質の良さで知られることが多い）",
    ),
    "recessive gene": (
        "劣性遺伝子",
        "Cystic fibrosis is caused by a recessive gene inherited from both parents."
        "（嚢胞性線維症は両親から受け継いだ劣性遺伝子によって引き起こされる）",
    ),
    "crop rotation": (
        "輪作",
        "Crop rotation helps maintain soil fertility and reduce pests."
        "（輪作は土壌の肥沃度を維持し害虫を減らすのに役立つ）",
    ),
    "chiefdom": (
        "首長制",
        "A chiefdom is a political unit led by a single chief."
        "（首長制は一人の首長によって率いられる政治単位だ）",
    ),
    "nasal cavity": (
        "鼻腔",
        "The nasal cavity warms and filters air before it reaches the lungs."
        "（鼻腔は空気が肺に達する前に温め、ろ過する）",
    ),
    "irrational number": (
        "無理数",
        "Pi (π) is an irrational number that cannot be expressed as a fraction."
        "（円周率πは分数で表せない無理数だ）",
    ),
    "gestation period": (
        "妊娠期間",
        "The gestation period of an elephant is about 22 months."
        "（ゾウの妊娠期間は約22ヶ月だ）",
    ),
    "binary star": (
        "連星",
        "Many stars in our galaxy are binary stars that orbit each other."
        "（銀河の多くの星は互いに公転する連星だ）",
    ),
    "perennial plant": (
        "多年生植物",
        "Roses are perennial plants that return and bloom year after year."
        "（バラは毎年繰り返し花を咲かせる多年生植物だ）",
    ),
    "income distribution": (
        "所得分布；所得分配",
        "Income distribution has become increasingly unequal in many countries."
        "（多くの国で所得分布はますます不平等になっている）",
    ),
    "citrus fruit": (
        "柑橘類",
        "Oranges and lemons are citrus fruits rich in vitamin C."
        "（オレンジとレモンはビタミンCが豊富な柑橘類だ）",
    ),
}


# ---------------------------------------------------------------------------
# ヘルパー関数
# ---------------------------------------------------------------------------


def clean_meaning_text(text: str) -> str:
    """意味テキストからノイズを除去する。"""
    text = re.sub(r"〔[^〕]+〕", "", text)  # 〔文脈修飾子〕
    text = re.sub(r"◆[^\n<【・]+", "", text)  # ◆ 注記
    text = re.sub(r"《[^》]+》\s*", "", text)  # 《ジャンル》
    text = re.sub(r"〈[^〉]+〉\s*", "", text)  # 〈俗〉〈米〉等
    text = re.sub(r"～[のをがにはでも]?", "", text)  # ～プレースホルダ
    text = re.sub(r"（[^）]{25,}）", "", text)  # 長い括弧注記
    text = text.replace("◆", "").replace("●", "")
    # スペースは1つに正規化（英語表記を含む可能性があるため削除しない）
    text = re.sub(r"[ \t]{2,}", " ", text).strip()
    text = text.strip("、。 ,")
    # 意味が長すぎる場合は最初の項目のみ残す（~20文字超で「、」区切りがある場合）
    if len(text) > 20 and "、" in text:
        text = text.split("、")[0]
    return text


def split_example_line(line: str) -> str:
    """
    '・English text 日本語テキスト' → 'English text（日本語テキスト）'

    分割ルール:
      - 英語部分の末尾（スペースまたは句点の直後）にある最初の CJK 文字を探す
      - 直前の文字が数字の場合（例：「9月」の「9」）はそこを起点としない
        → さらに前の位置（スペース/句点直後）を使う
    """
    text = line.lstrip("・").strip()

    # 対話形式は短縮して返す
    if text.count('"') >= 4:
        return text[:150] + "…" if len(text) > 150 else text

    def is_cjk(ch: str) -> bool:
        cp = ord(ch)
        return (
            0x3000 <= cp <= 0x9FFF or 0xF900 <= cp <= 0xFAFF or 0x20000 <= cp <= 0x2A6DF
        )

    ja_start = -1
    for i, ch in enumerate(text):
        if i < 5:
            continue
        if not is_cjk(ch):
            continue
        # 直前が数字の場合は「9月」等の誤分割を防ぐため、
        # その前のスペース/句点位置まで遡る
        candidate = i
        while candidate > 5 and text[candidate - 1].isdigit():
            candidate -= 1
        # スペースか句点の直後でないと分割しない
        if candidate > 0 and text[candidate - 1] not in " .!?,、。":
            continue
        ja_start = candidate
        break

    if ja_start == -1:
        return text

    en_part = text[:ja_start].strip().rstrip(". ")
    ja_part = text[ja_start:].strip().rstrip("。")
    if not en_part or not ja_part:
        return text
    return f"{en_part}.（{ja_part}）"


def is_noise_tag(tag: str) -> bool:
    """スキップすべき辞書タグかどうか判定する。"""
    noise_keywords = ["＠", "変化", "分節", "用法", "類", "同", "反", "参考", "対"]
    return any(kw in tag for kw in noise_keywords)


def extract_pos_num(tag: str) -> tuple[str, int]:
    """
    '名-1' → ('名', 1),  '他動-2' → ('他動', 2),  '自動' → ('自動', 1)
    自動と他動は区別して返す（意味の優先順位付けに使う）。
    """
    num_match = re.search(r"-(\d+)$", tag)
    num = int(num_match.group(1)) if num_match else 1

    if "名" in tag:
        pos = "名"
    elif "他動" in tag:
        pos = "他動"
    elif "自動" in tag:
        pos = "自動"
    elif "動" in tag:
        pos = "動"
    elif "形" in tag:
        pos = "形"
    elif "副" in tag:
        pos = "副"
    elif "略" in tag:
        pos = "略"
    elif "前" in tag:
        pos = "前"
    else:
        pos = ""
    return pos, num


# 品詞の表示優先順（自動より他動を優先、名・形・副も1個ずつ）
_POS_PRIORITY = ["他動", "自動", "動", "名", "形", "副", "略", "前", ""]


def parse_dict_format(text: str) -> tuple[list[tuple[str, str]], list[str]]:
    """
    【】マークアップ形式テキストから
    - (品詞ラベル, 意味テキスト) のリスト
    - 例文のリスト
    を抽出する。

    意味の採用ルール:
      - 品詞グループが1種類のみ → その品詞から最大2個
      - 品詞グループが2種類以上 → 各品詞から最大1個、合計最大3グループ
    """
    segments = re.split(r"<br>\s*", text)
    # (pos, num, meaning) で収集してから後で絞り込む
    collected: list[tuple[str, int, str]] = []
    examples: list[str] = []

    for seg in segments:
        seg = seg.strip().lstrip("、")
        if not seg:
            continue

        # 例文行
        if seg.startswith("・"):
            # 対話形式（"..." "..." が連続）はスキップ
            if seg.count('"') >= 4:
                continue
            # 長すぎる例文はスキップ
            if len(seg) > 200:
                continue
            if len(examples) < 2:
                examples.append(seg)
            continue

        # 【タグ】内容 形式
        tag_match = re.match(r"【([^】]+)】(.*)", seg, re.DOTALL)
        if not tag_match:
            continue

        tag = tag_match.group(1)
        content = tag_match.group(2).strip()

        if is_noise_tag(tag):
            continue

        pos, num = extract_pos_num(tag)
        meaning = clean_meaning_text(content)
        if not meaning:
            continue

        collected.append((pos, num, meaning))

    # 品詞グループを取得（順序保持）
    seen_pos: list[str] = []
    for pos, _, _ in collected:
        if pos not in seen_pos:
            seen_pos.append(pos)

    n_pos_groups = len(seen_pos)

    meanings: list[tuple[str, str]] = []
    pos_taken: dict[str, int] = {}

    for pos, num, meaning in collected:
        taken = pos_taken.get(pos, 0)
        # 品詞グループ数に応じた上限
        if n_pos_groups == 1:
            limit = 2  # 単一品詞なら2個まで
        else:
            limit = 1  # 複数品詞なら各1個

        if taken >= limit:
            continue

        # 品詞グループは最大3つまで
        unique_pos_in_meanings = len({p for p, _ in meanings})
        if pos not in {p for p, _ in meanings} and unique_pos_in_meanings >= 3:
            continue

        meanings.append((pos, meaning))
        pos_taken[pos] = taken + 1

    return meanings, examples


# 表示用に自動/他動をまとめて「動」と表示する
_POS_DISPLAY = {"自動": "動", "他動": "動"}


def format_card_back(
    meanings: list[tuple[str, str]],
    examples: list[str],
) -> str:
    """意味リストと例文リストを Anki カード裏面テキストに整形する。"""
    # 品詞グループごとに意味をまとめる（自動・他動は「動」に統合）
    pos_groups: dict[str, list[str]] = {}
    order: list[str] = []
    for pos, m in meanings:
        display_pos = _POS_DISPLAY.get(pos, pos)
        if display_pos not in pos_groups:
            pos_groups[display_pos] = []
            order.append(display_pos)
        pos_groups[display_pos].append(m)

    meaning_parts = []
    for pos in order:
        ms = pos_groups[pos]
        joined = "；".join(ms)
        if pos:
            meaning_parts.append(f"（{pos}）{joined}")
        else:
            meaning_parts.append(joined)

    meaning_str = "　".join(meaning_parts)

    # 例文を整形（最大2つ）
    example_strs = []
    for ex in examples[:2]:
        formatted = split_example_line(ex)
        if formatted:
            example_strs.append(formatted)

    if example_strs:
        ex_block = "<br>".join(f"例：{e}" for e in example_strs)
        return f"{meaning_str}<br>{ex_block}"
    else:
        return meaning_str


def transform_back(word: str, back: str) -> str:
    """単語と裏面テキストを受け取り、整形された裏面テキストを返す。"""

    has_markup = any(c in back for c in ["【", "◆", "●"])
    has_example = "・" in back or "<br>" in back

    # ── ケース1: シンプルエントリ（マークアップなし・例文なし） ──
    if not has_markup and not has_example:
        if word in SIMPLE_EXAMPLES:
            meaning, example = SIMPLE_EXAMPLES[word]
            return f"{meaning}<br>例：{example}"
        # 辞書未登録はそのまま
        return back

    # ── ケース2: 【】マークアップ形式 ──
    if has_markup:
        meanings, examples = parse_dict_format(back)
        if not meanings and not examples:
            # パース失敗時は最低限のノイズ除去のみ
            cleaned = re.sub(r"<br>【[＠変分][^<]*", "", back)
            cleaned = re.sub(r"【[＠変分][^】]*】[^<\n【]*", "", cleaned)
            return cleaned.strip("<br> ")
        return format_card_back(meanings, examples)

    # ── ケース3: <br> のみで区切られている（既存の整形済み or 例文あり） ──
    return back


# ---------------------------------------------------------------------------
# メイン処理
# ---------------------------------------------------------------------------


def main() -> None:
    if not INPUT.exists():
        print(f"入力ファイルが見つかりません: {INPUT}")
        return

    with open(INPUT, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    try:
        back_idx = header.index("裏面")
        word_idx = header.index("表面")
    except ValueError:
        # BOM付きヘッダーのフォールバック
        stripped = [h.lstrip("\ufeff") for h in header]
        try:
            back_idx = stripped.index("裏面")
            word_idx = stripped.index("表面")
        except ValueError:
            print(f"ヘッダーに '表面' / '裏面' が見つかりません: {header}")
            return

    transformed_rows: list[list[str]] = []
    changed = 0

    for row in rows:
        new_row = row.copy()
        if len(row) > max(back_idx, word_idx):
            word = row[word_idx]
            original_back = row[back_idx]
            new_back = transform_back(word, original_back)
            if new_back != original_back:
                changed += 1
            new_row[back_idx] = new_back
        transformed_rows.append(new_row)

    with open(OUTPUT, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(transformed_rows)

    print(f"完了: {len(transformed_rows)} 行処理, {changed} 行変更")
    print(f"出力: {OUTPUT}")


if __name__ == "__main__":
    main()
