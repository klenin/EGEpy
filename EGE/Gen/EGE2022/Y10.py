from dataclasses import dataclass

from EGE.GenBase import DirectInput


class SearchWithTextEditor(DirectInput):
    @dataclass
    class DocumentInfo:
        name: str
        path: str
        words: list

class SearchInLiteraryWork(SearchWithTextEditor):
    @dataclass
    class AuthorInfo:
        name: str
        genitive_name: str
        works: list

    @dataclass
    class WorkInfo(SearchWithTextEditor.DocumentInfo):
        dativ_type: str = ""
        genitive_type: str = ""

class SearchStrictFormOfWord(SearchInLiteraryWork):
    authorsList = [
        SearchInLiteraryWork.AuthorInfo("А. С. Пушкин", "А. С. Пушкина", [
            SearchInLiteraryWork.WorkInfo("Евгений Онегин", "", [
                "долг", "ты", "вы", "север", "свет", "день", "дом", "Онегин", "его", "она", "чёрт", "сад", "звук", "мы", "всё", "был",
            ], dativ_type="стихах"),
        ]),
    ]

class SearchAnyFormOfWord(SearchInLiteraryWork):
    authorsList = [
        SearchInLiteraryWork.AuthorInfo("А. С. Пушкин", "А. С. Пушкина", [
            SearchInLiteraryWork.WorkInfo(
                "Капитанская дочка",
                "",
                [ "дочка", "капитанская", "Емельян", "картина", "Москва", "Александр", "арест", "граф" ],
            ),
            SearchInLiteraryWork.WorkInfo("Дубровский", "", [ "ключ", "пир", "застава", "борода", ]),
        ]),
        SearchInLiteraryWork.AuthorInfo("Н. В. Гоголь", "Н. В. Гоголя", [
            SearchInLiteraryWork.WorkInfo("Нос", "", [ "полный", "шерсть", ])
        ]),
        SearchInLiteraryWork.AuthorInfo("А. С. Грибоедов", "А. С. Грибоедова", [
            SearchInLiteraryWork.WorkInfo("Горе от ума", "", [ "батюшка", "борода", ])
        ]),
    ]

class SearchWordWithFirstCapitalLetter(SearchInLiteraryWork):
    authorsList = [
        SearchInLiteraryWork.AuthorInfo("Н. А. Некрасов", "Н. А. Некрасова", [
            SearchInLiteraryWork.WorkInfo("Кому на Руси жить хорошо", "", [ "Мой", ], True, genitive_type="поэмы")
        ]),
    ]
