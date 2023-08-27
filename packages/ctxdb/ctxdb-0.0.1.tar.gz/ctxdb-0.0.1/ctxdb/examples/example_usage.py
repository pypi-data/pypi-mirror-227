from ctxdb.core.ctxdb import ContextDB
from ctxdb.models.context import BaseContext
from ctxdb.utils import encode


class ContextManager:

    def __init__(self, db_type="in_memory"):
        self.ctxdb = ContextDB(db_type=db_type)

    def add_context(self, input_text, output_text):
        context = BaseContext(input=input_text,
                              embedding=encode(input_text),
                              output=output_text)
        self.ctxdb.add_context(context)

    def query(self, query_text):
        query_ctx = BaseContext(input=query_text, embedding=encode(query_text))
        matches, scores = self.ctxdb.search_context(query_ctx,
                                                    search_field='embedding',
                                                    limit=5)
        return matches[0].output, scores


def create_sample_contexts(context_manager):
    sample_data = [
        ("What is a Photon-Matter Converter?",
         "A Photon-Matter Converter is a fictional device that transforms light energy into solid matter, often used in advanced 4D printing technology."
         ),
        ("Who was Emperor Caelux?",
         "Emperor Caelux was a mythical ruler in the kingdom of Eldoria, famous for unifying the seven realms through diplomacy rather than war."
         ),
        ("What is a Skorn?",
         "A Skorn is a mythical creature inhabiting the enchanted forests of Veridia."
         ),
        ("What does Elixirium Vitae do?",
         "Elixirium Vitae is a fictional potion concocted by the alchemist Isolde the Wise."
         ),
        ("How does the Enchanted Exchange work?",
         "The Enchanted Exchange is a magical marketplace that appears only during a lunar eclipse."
         )
    ]

    for input_text, output_text in sample_data:
        context_manager.add_context(input_text, output_text)


def main():
    context_manager = ContextManager()
    create_sample_contexts(context_manager)

    query_text = input("Enter a query: ")
    answer, scores = context_manager.query(query_text)

    print(f'Question: {query_text}')
    print(f'Answer: {answer}')
    print(f'Scores: {scores}')


if __name__ == "__main__":
    main()
