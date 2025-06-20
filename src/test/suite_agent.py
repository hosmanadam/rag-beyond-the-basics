"""
Evaluate generator (agent_1)

Please read this book in full, with great attention: @frank_hardys_choice.txt

Now understand that I am creating a research project about Retrieval Augmented Generation. I want to create a test case for a RAG agent consisting of a question which is impossible to answer accurately by merely reading this book or retrieving chunks from it. The question must require retrieving information from this book and then, based on that information, searching the Internet for recent obscure information. It's acceptable if the question is not realistic, but it should technically prove that a simple rag tool which just retrieves from the book is not able to answer, while an agent that can first read from the book and then search the internet is able to answer.

Please generate 10 such test cases.

Additional criteria:
- The test cases should adhere to this format: @suite_general_A.py
- Save the test cases here: @suite_book_hybrid_rag.py
- The question MUST NOT give sufficient information for the web search. Multiple hops must be required. First book reading, then web search.
- There should be three comments for each test case:
    1. Explains why the test case satisfies the technical criteria
    2. Provides exact quotes from the book to verify the first hop
    3. Provides exact URL from the web resource to verify the second hop
- You need to search the internet in each case to be able to figure out the correct expected_output.
- It is currently 2025-06-20. Rely on the most recent possible information.

Here is a good example, please start with this one and then generate more: "If someone in the UK in 2025 would be convicted for the same offense as Frank Hardy in the book, what would be the likely punishment under current UK law, and how does this compare to what Frank actually received?"

Please start.
"""

import logging

from deepeval import evaluate
from deepeval.evaluate import AsyncConfig, DisplayConfig
from deepeval.test_case import LLMTestCase
from dotenv import load_dotenv
from langchain_core.runnables import Runnable

# from src.main.rag import agent_1 as app
from src.main.rag import book_6 as app
from src.main.util.responses import get_response
from src.test.metrics import correctness_metric

_logger = logging.getLogger(__name__)


def create_test_cases(chain: Runnable) -> list[LLMTestCase]:
    # Test Case 1: UK sentencing comparison
    question = "If someone in the UK in 2025 would be convicted for the same offense as Frank Hardy in the book, what would be the likely punishment under current UK law, and how does this compare to what Frank actually received?"
    tc1 = LLMTestCase(
        input=question,
        expected_output="Under current UK law (2025), Frank Hardy would likely face a sentence ranging from community service to up to 14 years' imprisonment for handling stolen goods, depending on the value and circumstances. Given that poached game would be considered low-value goods (under £1,000), Frank would likely receive a Band B to Band C fine or low-level community order under current guidelines. This is significantly more lenient than Frank's actual sentence of 2 years' imprisonment with hard labour, reflecting the evolution of UK sentencing practices toward rehabilitation over purely punitive measures.",
        actual_output=get_response(question, chain),
        # 1. Technical criteria: Requires first finding Frank's offense (receiving stolen poached game) and sentence (2 years hard labour) from book, then searching current UK sentencing guidelines
        # 2. Book quote: "Frank Hardy, as the receiver of property known to have been stolen, was sentenced to two years' imprisonment, with hard labour."
        # 3. Web verification: https://www.sentencingcouncil.org.uk/offences/magistrates-court/item/handling-stolen-goods-2/ - current UK sentencing guidelines for handling stolen goods
    )

    # Test Case 2: Modern apprenticeship comparison  
    question = "What is the minimum wage for apprentices in the UK in 2025, and how would this compare to what Walter and Frank earned as carpenter apprentices?"
    tc2 = LLMTestCase(
        input=question,
        expected_output="The UK apprentice minimum wage in 2025 is £7.55 per hour for apprentices under 19 or those in their first year (increased from £6.40 in April 2025). Walter and Frank earned money from 'working overtime' as apprentices, but their exact wages aren't specified in the book. However, the book indicates they had limited pocket money and Walter could barely afford evening school expenses, suggesting their earnings were minimal compared to modern apprentice wages which would provide significantly better financial security.",
        actual_output=get_response(question, chain),
        # 1. Technical criteria: Requires identifying Walter and Frank as carpenter apprentices from book, then searching current UK apprentice minimum wage rates
        # 2. Book quote: "Walter and Frank were both apprentices, and any little money they earned was for working overtime."
        # 3. Web verification: https://www.gov.uk/apprenticeship-minimum-wage - current UK apprentice minimum wage rates for 2025
    )

    # Test Case 3: Evening school vs modern adult education
    question = "What are the current costs for adult evening classes in the UK in 2025, and how does this compare to the evening school Walter attended?"
    tc3 = LLMTestCase(
        input=question,
        expected_output="Adult evening classes in the UK in 2025 typically cost between £50-£300 per course depending on the subject and institution, with many free courses available through adult education providers. Walter's evening school was free, established by the rector and local gentlemen as a community service. This represents a significant shift from Victorian-era philanthropic education to modern publicly funded adult learning, though free options still exist through libraries and community centers.",
        actual_output=get_response(question, chain),
        # 1. Technical criteria: Requires finding details about Walter's free evening school from book, then searching current UK adult education costs
        # 2. Book quote: "Walter felt that his mother would not have to put her hand in her pocket to pay for his attendance at the evening school, and he knew that he could not spend his pocket-money in a better way."
        # 3. Web verification: https://www.gov.uk/government/organisations/education-and-skills-funding-agency - current adult education funding and costs
    )

    # Test Case 4: Poaching penalties comparison
    question = "What are the current penalties for poaching in the UK in 2025, and how do they compare to what Tom Haines received?"
    tc4 = LLMTestCase(
        input=question,
        expected_output="Current UK poaching penalties under the Game Act 1831 and Night Poaching Act 1828 (as updated by the Police, Crime, Sentencing and Courts Act 2022) include unlimited fines and/or up to 6 months imprisonment. Tom Haines received 5 years' penal servitude for poaching. Modern penalties are significantly lighter, with maximum 6 months custody compared to his 5-year sentence, reflecting the evolution from Victorian-era harsh punishments to modern proportionate sentencing focused on deterrence rather than lengthy imprisonment.",
        actual_output=get_response(question, chain),
        # 1. Technical criteria: Requires finding Tom Haines' sentence for poaching from book, then searching current UK poaching penalties
        # 2. Book quote: "Tom Haines, who was not proved to have used violence, was condemned to five years' penal servitude"
        # 3. Web verification: https://www.legislation.gov.uk/ukpga/1831/32 - current UK poaching laws and penalties
    )

    # Test Case 5: Savings account interest comparison
    question = "What is the current interest rate for Post Office Savings Bank accounts in the UK in 2025, and how does this compare to Walter's experience?"
    tc5 = LLMTestCase(
        input=question,
        expected_output="The Post Office Savings Bank no longer exists as it was privatized and became part of NS&I (National Savings and Investments). Current NS&I accounts in 2025 offer variable interest rates typically between 0.1-4.5% depending on the product. Walter deposited his first earnings (5 shillings) in the Post Office Savings Bank, which historically offered secure but modest returns. Modern NS&I products offer similar security but with rates that fluctuate with economic conditions.",
        actual_output=get_response(question, chain),
        # 1. Technical criteria: Requires finding Walter's use of Post Office Savings Bank from book, then searching current NS&I/Post Office savings rates
        # 2. Book quote: "put that five shillings into the Post-Office Savings' Bank this very evening, Walter, as the first fruits of the benefit you have reaped"
        # 3. Web verification: https://www.nsandi.com/ - current National Savings and Investments rates and products
    )

    # Test Case 6: Transportation vs modern deportation
    question = "What are the current UK policies on deportation for violent crimes in 2025, and how do they compare to Turner's sentence of transportation?"
    tc6 = LLMTestCase(
        input=question,
        expected_output="Turner received 20 years' transportation for wounding a gamekeeper, which was effectively permanent exile. Modern UK deportation policy under the Immigration Act 2014 allows deportation of foreign nationals for serious crimes, but British citizens cannot be deported. Transportation was abolished in 1868. Modern equivalent sentences for grievous bodily harm range from 3-16 years imprisonment, with deportation only possible for non-citizens after serving their sentence.",
        actual_output=get_response(question, chain),
        # 1. Technical criteria: Requires finding Turner's sentence of 20 years transportation from book, then searching current UK deportation policies
        # 2. Book quote: "Turner, who had wounded one of the gamekeepers, and had been committed on a previous occasion, was sentenced to twenty years' transportation."
        # 3. Web verification: https://www.legislation.gov.uk/ukpga/2014/22 - current UK Immigration Act and deportation policies
    )

    # Test Case 7: Carpentry training comparison
    question = "What are the current requirements and costs for carpentry apprenticeships in the UK in 2025, and how do they compare to Walter and Frank's experience?"
    tc7 = LLMTestCase(
        input=question,
        expected_output="Modern UK carpentry apprenticeships in 2025 are typically Level 2 or 3 qualifications lasting 2-4 years, with apprentices earning at least £6.40/hour and receiving formal training. Walter and Frank served traditional apprenticeships under Mr. King with no formal qualifications mentioned. Modern apprenticeships include college-based learning, workplace training, and recognized qualifications, representing a significant formalization of the trade training process compared to the informal master-apprentice system of the Victorian era.",
        actual_output=get_response(question, chain),
        # 1. Technical criteria: Requires finding details of Walter and Frank's carpentry apprenticeship from book, then searching current UK apprenticeship requirements
        # 2. Book quote: "Walter and Frank were both learning the trade of a carpenter, and worked together at the same bench."
        # 3. Web verification: https://www.gov.uk/apprenticeships-guide - current UK apprenticeship structure and requirements
    )

    # Test Case 8: Alcohol licensing laws comparison
    question = "What are the current UK licensing laws for public houses in 2025, and how do they compare to 'The Plough' mentioned in the book?"
    tc8 = LLMTestCase(
        input=question,
        expected_output="Modern UK pub licensing under the Licensing Act 2003 allows flexible opening hours (often 11am-11pm or later) with strict regulations on serving alcohol. 'The Plough' in the book operated under Victorian licensing laws with more restrictive hours but less regulation of consumption. Modern laws focus on preventing antisocial behavior and protecting public health, with premises licenses, personal licenses, and strict penalties for serving intoxicated persons - a significant evolution from the Victorian era's more laissez-faire approach.",
        actual_output=get_response(question, chain),
        # 1. Technical criteria: Requires finding references to 'The Plough' public house from book, then searching current UK pub licensing laws
        # 2. Book quote: "There was a roadside public-house, called 'The Plough,' not far from the mill; and there John Hardy spent a good part of his weekly earning."
        # 3. Web verification: https://www.legislation.gov.uk/ukpga/2003/17 - current UK Licensing Act governing public houses
    )

    # Test Case 9: Child labor laws comparison
    question = "What are the current UK laws regarding children working in 2025, and how do they compare to the child employment described in the book?"
    tc9 = LLMTestCase(
        input=question,
        expected_output="Current UK child employment laws (Children and Young Persons Act 1933, updated 2023) prohibit children under 13 from working, with strict restrictions for 13-16 year olds including maximum hours and prohibited dangerous work. The book mentions children leaving school at 9-12 years old to work. Modern laws mandate education until 18 and severely restrict child labor, representing a fundamental shift from Victorian practices where child labor was common and necessary for family survival.",
        actual_output=get_response(question, chain),
        # 1. Technical criteria: Requires finding references to children leaving school early to work from book, then searching current UK child employment laws
        # 2. Book quote: "the working-classes withdraw their children from school as soon as their labour can be turned to any account, so that, with very few exceptions, all education may be said to have ceased before the age of twelve"
        # 3. Web verification: https://www.legislation.gov.uk/ukpga/1933/12 - current UK Children and Young Persons Act regulating child employment
    )

    # Test Case 10: Railway development comparison
    question = "What is the current status of railway development in small UK coastal villages in 2025, and how does this compare to Springcliffe's transformation?"
    tc10 = LLMTestCase(
        input=question,
        expected_output="Many small UK coastal villages in 2025 have limited or no railway connections due to the Beeching cuts of the 1960s, though some have benefited from heritage railways or light rail systems. Springcliffe became 'a place of great importance' when the railway passed within a quarter mile, spurring building development. Modern coastal villages often rely on road transport and tourism, with railway development now focused on high-speed intercity routes rather than rural branch lines, reversing much of the Victorian expansion that transformed places like Springcliffe.",
        actual_output=get_response(question, chain),
        # 1. Technical criteria: Requires finding information about Springcliffe's railway development from book, then searching current UK rural railway status
        # 2. Book quote: "Springcliffe had, by that time, become a place of great importance, in consequence of the railway passing within a quarter of a mile of the village."
        # 3. Web verification: https://www.networkrail.co.uk/ - current UK railway network and rural connections
    )

    return [tc1, tc2, tc3, tc4, tc5, tc6, tc7, tc8, tc9, tc10]


def evaluate_test_cases():
    _logger.info("Creating test cases...")
    chain = app.create_chain()
    test_cases = create_test_cases(chain)
    _logger.info(f"Evaluating {len(test_cases)} test cases...")
    evaluate(
        test_cases=test_cases,
        metrics=[correctness_metric],
        async_config=AsyncConfig(max_concurrent=1, run_async=False),
        display_config=DisplayConfig(show_indicator=False),
    )


if __name__ == "__main__":
    load_dotenv()
    evaluate_test_cases()
