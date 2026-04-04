export const CAREER_TEST_COLUMNS = [
  { id: 'I', label: 'I' },
  { id: 'II', label: 'II' },
  { id: 'III', label: 'III' },
  { id: 'IV', label: 'IV' },
  { id: 'V', label: 'V' },
  { id: 'VI', label: 'VI' },
]

export const CAREER_TEST_QUESTIONS = [
  {
    id: 1,
    title: 'Мне хотелось бы в своей профессиональной деятельности',
    options: [
      { key: 'a', label: 'общаться с самыми разными людьми', column: 'I', prefix: 'а' },
      { key: 'b', label: 'снимать фильмы, писать книги, рисовать, выступать на сцене и т.д.', column: 'IV', prefix: 'б' },
      { key: 'c', label: 'заниматься расчетами; вести документацию', column: 'VI', prefix: 'в' },
    ],
  },
  {
    id: 2,
    title: 'В книге или кинофильме меня больше всего привлекает',
    options: [
      { key: 'a', label: 'возможность следить за ходом мыслей автора', column: 'II', prefix: 'а' },
      { key: 'b', label: 'художественная форма, мастерство писателя или режиссера', column: 'IV', prefix: 'б' },
      { key: 'c', label: 'сюжет, действия героев', column: 'V', prefix: 'в' },
    ],
  },
  {
    id: 3,
    title: 'Меня больше обрадует Нобелевская премия',
    options: [
      { key: 'a', label: 'за общественную деятельность', column: 'I', prefix: 'а' },
      { key: 'b', label: 'в области наук', column: 'II', prefix: 'б' },
      { key: 'c', label: 'в области искусства', column: 'IV', prefix: 'в' },
    ],
  },
  {
    id: 4,
    title: 'Я скорее соглашусь стать',
    options: [
      { key: 'a', label: 'главным механиком', column: 'III', prefix: 'а' },
      { key: 'b', label: 'начальником экспедиции', column: 'V', prefix: 'б' },
      { key: 'c', label: 'главным бухгалтером', column: 'VI', prefix: 'в' },
    ],
  },
  {
    id: 5,
    title: 'Будущее людей определяют',
    options: [
      { key: 'a', label: 'взаимопонимание между людьми', column: 'I', prefix: 'а' },
      { key: 'b', label: 'научные открытия', column: 'II', prefix: 'б' },
      { key: 'c', label: 'развитие производства', column: 'III', prefix: 'в' },
    ],
  },
  {
    id: 6,
    title: 'Если я стану руководителем, то в первую очередь займусь',
    options: [
      { key: 'a', label: 'созданием дружного, сплоченного коллектива', column: 'I', prefix: 'а' },
      { key: 'b', label: 'разработкой новых технологий обучения', column: 'II', prefix: 'б' },
      { key: 'c', label: 'работой с документами', column: 'VI', prefix: 'в' },
    ],
  },
  {
    id: 7,
    title: 'На технической выставке меня больше привлечет',
    options: [
      { key: 'a', label: 'внутреннее устройство экспонатов', column: 'II', prefix: 'а' },
      { key: 'b', label: 'их практическое применение', column: 'III', prefix: 'б' },
      { key: 'c', label: 'внешний вид экспонатов (цвет, форма)', column: 'IV', prefix: 'в' },
    ],
  },
  {
    id: 8,
    title: 'В людях я ценю, прежде всего',
    options: [
      { key: 'a', label: 'дружелюбие и отзывчивость', column: 'I', prefix: 'а' },
      { key: 'b', label: 'смелость и выносливость', column: 'V', prefix: 'б' },
      { key: 'c', label: 'обязательность и аккуратность', column: 'VI', prefix: 'в' },
    ],
  },
  {
    id: 9,
    title: 'В свободное время мне хотелось бы',
    options: [
      { key: 'a', label: 'ставить различные опыты, эксперименты', column: 'II', prefix: 'а' },
      { key: 'b', label: 'писать стихи, сочинять музыку или рисовать', column: 'IV', prefix: 'б' },
      { key: 'c', label: 'тренироваться', column: 'V', prefix: 'в' },
    ],
  },
  {
    id: 10,
    title: 'В заграничных поездках меня скорее заинтересует',
    options: [
      { key: 'a', label: 'возможность знакомства с историей и культурой другой страны', column: 'IV', prefix: 'а' },
      { key: 'b', label: 'экстремальный туризм (альпинизм, виндсерфинг, горные лыжи)', column: 'V', prefix: 'б' },
      { key: 'c', label: 'деловое общение', column: 'VI', prefix: 'в' },
    ],
  },
  {
    id: 11,
    title: 'Мне интереснее беседовать о',
    options: [
      { key: 'a', label: 'человеческих взаимоотношениях', column: 'I', prefix: 'а' },
      { key: 'b', label: 'новой научной гипотезе', column: 'II', prefix: 'б' },
      { key: 'c', label: 'технических характеристиках новой модели машины, компьютера', column: 'III', prefix: 'в' },
    ],
  },
  {
    id: 12,
    title: 'Если бы в моей школе было всего три кружка, я бы выбрал',
    options: [
      { key: 'a', label: 'технический', column: 'III', prefix: 'а' },
      { key: 'b', label: 'музыкальный', column: 'IV', prefix: 'б' },
      { key: 'c', label: 'спортивный', column: 'V', prefix: 'в' },
    ],
  },
  {
    id: 13,
    title: 'В школе следует обратить особое внимание на',
    options: [
      { key: 'a', label: 'улучшение взаимопонимания между учителями и учениками', column: 'I', prefix: 'а' },
      { key: 'b', label: 'поддержание здоровья учащихся, занятия спортом', column: 'V', prefix: 'б' },
      { key: 'c', label: 'укрепление дисциплины', column: 'VI', prefix: 'в' },
    ],
  },
  {
    id: 14,
    title: 'Я с большим удовольствием смотрю',
    options: [
      { key: 'a', label: 'научно-популярные фильмы', column: 'II', prefix: 'а' },
      { key: 'b', label: 'программы о культуре и искусстве', column: 'IV', prefix: 'б' },
      { key: 'c', label: 'спортивные программы', column: 'V', prefix: 'в' },
    ],
  },
  {
    id: 15,
    title: 'Мне хотелось бы работать',
    options: [
      { key: 'a', label: 'с детьми или сверстниками', column: 'I', prefix: 'а' },
      { key: 'b', label: 'с машинами, механизмами', column: 'III', prefix: 'б' },
      { key: 'c', label: 'с объектами природы', column: 'V', prefix: 'в' },
    ],
  },
  {
    id: 16,
    title: 'Школа в первую очередь должна',
    options: [
      { key: 'a', label: 'учить общению с другими людьми', column: 'I', prefix: 'а' },
      { key: 'b', label: 'давать знания', column: 'III', prefix: 'б' },
      { key: 'c', label: 'обучать навыкам работы', column: 'VI', prefix: 'в' },
    ],
  },
  {
    id: 17,
    title: 'Главное в жизни',
    options: [
      { key: 'a', label: 'иметь возможность заниматься творчеством', column: 'IV', prefix: 'а' },
      { key: 'b', label: 'вести здоровый образ жизни', column: 'V', prefix: 'б' },
      { key: 'c', label: 'тщательно планировать свои дела', column: 'VI', prefix: 'в' },
    ],
  },
  {
    id: 18,
    title: 'Государство должно в первую очередь заботиться о',
    options: [
      { key: 'a', label: 'защите интересов и прав граждан', column: 'I', prefix: 'а' },
      { key: 'b', label: 'достижениях в области науки и техники', column: 'II', prefix: 'б' },
      { key: 'c', label: 'материальном благополучии граждан', column: 'III', prefix: 'в' },
    ],
  },
  {
    id: 19,
    title: 'Мне больше всего нравятся уроки',
    options: [
      { key: 'a', label: 'труда', column: 'III', prefix: 'а' },
      { key: 'b', label: 'физкультуры', column: 'V', prefix: 'б' },
      { key: 'c', label: 'математики', column: 'VI', prefix: 'в' },
    ],
  },
  {
    id: 20,
    title: 'Мне интереснее было бы',
    options: [
      { key: 'a', label: 'заниматься сбытом товаров', column: 'I', prefix: 'а' },
      { key: 'b', label: 'изготавливать изделия', column: 'III', prefix: 'б' },
      { key: 'c', label: 'планировать производство товаров', column: 'VI', prefix: 'в' },
    ],
  },
  {
    id: 21,
    title: 'Я предпочитаю читать статьи о',
    options: [
      { key: 'a', label: 'выдающихся ученых и их открытиях', column: 'II', prefix: 'а' },
      { key: 'b', label: 'интересных изобретениях', column: 'III', prefix: 'б' },
      { key: 'c', label: 'жизни и творчестве писателей, художников, музыкантов', column: 'IV', prefix: 'в' },
    ],
  },
  {
    id: 22,
    title: 'Свободное время я люблю',
    options: [
      { key: 'a', label: 'читать, думать, рассуждать', column: 'II', prefix: 'а' },
      { key: 'b', label: 'что-нибудь мастерить, шить, ухаживать за животными, растениями', column: 'III', prefix: 'б' },
      { key: 'c', label: 'ходить на выставки, концерты, в музеи', column: 'IV', prefix: 'в' },
    ],
  },
  {
    id: 23,
    title: 'Больший интерес у меня вызовет сообщение о',
    options: [
      { key: 'a', label: 'научном открытии', column: 'II', prefix: 'а' },
      { key: 'b', label: 'художественной выставке', column: 'IV', prefix: 'б' },
      { key: 'c', label: 'экономической ситуации', column: 'VI', prefix: 'в' },
    ],
  },
  {
    id: 24,
    title: 'Я предпочту работать',
    options: [
      { key: 'a', label: 'в помещении, где много людей', column: 'I', prefix: 'а' },
      { key: 'b', label: 'в необычных условиях', column: 'V', prefix: 'б' },
      { key: 'c', label: 'в обычном кабинете', column: 'VI', prefix: 'в' },
    ],
  },
]

export const CAREER_TEST_SUMMARY = {
  about:
    'Вы быстро вовлекаетесь в новые задачи, лучше понимаете свои сильные стороны и можете опираться на них при выборе дальнейшего направления.',
  directions:
    'После регистрации мы покажем подробную интерпретацию результатов теста, персональный план развития и подходящие карьерные направления.',
}
