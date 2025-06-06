!pip install dspy
import dspy
from dspy import InputField, OutputField
import pandas as pd
from tqdm import tqdm
from sklearn.model_selection import train_test_split

openai_api_key = ""
lm = dspy.LM(model="gpt-4o-mini", api_key=openai_api_key)
dspy.settings.configure(lm=lm)

binary_political_interest = True

question_and_answer = {
    'race': {
        "template":"Race: XXX",
        "valmap":{ 1:'White.', 2:'Black.', 3:'Asian.', 4:'Native American.', 5:'Hispanic.' },
        },
    'age': {
        "template":"Age: XXX years old.",
        "valmap":{},
        },
    'bible_truth': {
        "template":"Feelings about the Bible: XXX",
        "valmap":{
        1:'The Bible is the actual word of God and is to be taken literally, word for word.',
        2:'The Bible is the word of God but not everything in it should be taken literally.',
        3:'The Bible is a book written by men and is not the word of God.'},
        },
    'attend_church': {
        "template":"Religious service attendance: XXX",
        "valmap":{
        1:'Yes.',
        2:'No.'},
        },
    'abortion_legality': {
        "template":"Opinion on abortion: XXX",
        "valmap":{
        1:'By law, abortion should never be permitted.',
        2:"By law, abortion should be permitted only in case of rape, incest, or when the woman's life in danger.",
        3:"By law, abortion should be permitted for reasons other than rape, incest, or when the woman's life in danger.",
        4:"By law, abortion should be permitted as a matter of personal choice."},
        },
    'ideology': {
        "template":"Party identification: XXX",
        "valmap":{
        1:'Strong Democrat.',
        2:"Not very strong Democrat.",
        3:"Independent but lean Democrat.",
        4:"Independent.",
        5:"Independent but lean Republican.",
        6:"Not very strong Republican.",
        7:"Strong Republican."},
        },
    'family_num': {
        "template":"Number of cohabiting family members: XXX",
        "valmap":{
        0:'Zero.',
        1:'One.',
        2:"Two.",
        3:"Three.",
        4:"Four.",
        5:"Five or more."},
        },
    'life_satisfaction': {
        "template":"Satisfaction with life: XXX",
        "valmap":{
        1:'Extremely satisfied.',
        2:"Very satisfied.",
        3:"Moderately satisfied.",
        4:"Slightly satisfied.",
        5:"Not satisfied at all."},
        },
    'health': {
        "template":"Health status: XXX",
        "valmap":{
        1:'Excellent.',
        2:"Very good.",
        3:"Good.",
        4:"Fair.",
        5:"Poor."},
        },
    'political_interest': {
        "template":"Interest in politics: XXX",
        "valmap":{
        1:'Very interested.',
        2:"Somewhat interested.",
        3:"Not very interested.",
        4:"Not at all interested."},
        },
    'trust': {
        "template":"Tendency to trust in others: XXX",
        "valmap":{
        1:'Always.',
        2:"Most of the time.",
        3:"About half the time.",
        4:"Some of the time.",
        5:"Never."},
        },
    'election_impact': {
        "template":"Effectiveness of election at holding governments accountable to public opinion: XXX",
        "valmap":{
        1:'A good deal.',
        2:"Some.",
        3:"Not much."},
        },
    'voting_duty': {
        "template":"Voting as duty or choice: XXX",
        "valmap":{
        1:'Very strongly a duty.',
        2:"Moderately strongly a duty.",
        3:"A little strongly a duty.",
        4:"Neither a duty nor a choice.",
        5:"A little strongly a choice.",
        6:"Moderately strongly a choice.",
        7:"Very strongly a choice."},
        },
    'immigration_policy': {
        "template":"Attitude toward unauthorized immigrants: XXX",
        "valmap":{
        1:'Make all unauthorized immigrants felons and send them back to their home country.',
        2:"Have a guest worker program that allows unauthorized immigrants to remain in the US.",
        3:"Allow unauthorized immigrants to remain in the US & eventually qualify for citizenship but only if they meet requirements.",
        4:"Allow unauthorized immigrants to remain in the US & eventually qualify for citizenship without penalties."},
        },
    'finance_next': {
        "template":"Relative to the current financial situation, the future situation will be: XXX",
        "valmap":{
        1:'Much better.',
        2:"Somewhat better.",
        3:"About the same.",
        4:"Somewhat worse.",
        5:"Much worse."},
        },
    'finance_past': {
        "template":"Relative to the past financial situation, the current situation is: XXX",
        "valmap":{
        1:'Much better.',
        2:"Somewhat better.",
        3:"About the same.",
        4:"Somewhat worse.",
        5:"Much worse."},
        },
    'environment_protection': {
        "template":"Level of federal spending on environmental protection: XXX",
        "valmap":{
        1:'Should be increased.',
        2:"Should be decreased.",
        3:"Should be kept the same."},
        },
    'campaign_interest': {
        "template":"Interest in political campaigns: XXX",
        "valmap":{
        1:'Very much interested.',
        2:"Somewhat interested.",
        3:"Not much interested."},
        },
    'welfare_spend': {
        "template":"Level of federal spending on welfare programs: XXX",
        "valmap":{
        1:'Should be increased.',
        2:"Should be decreased.",
        3:"Should be kept the same."},
        },
    'gun_control': {
        "template":"Laws on gun acquisition: XXX",
        "valmap":{
        1:'Should be made more stringent.',
        2:"Should be made less stringent.",
        3:"Should be kept the same."},
        },
    'discuss_politics': {
        "template":"Discusses politics with family and friends: XXX",
        "valmap":{
        1:'Yes.',
        2:"No."},
        },
    'gender': {
        "template":"Gender: XXX",
        "valmap":{
        1:'Male.',
        2:"Female."},
        },
    'region': {
        "template":"Physical location: XXX",
        "valmap":{
        1:'U.S. Northeast.',
        2:"U.S. Midwest.",
        3:"U.S. South.",
        4:"U.S. West."},
        },
    'congress_approval': {
        "template":"Congressional job approval: XXX",
        "valmap":{
        1:'Approve.',
        2:"Disapprove."},
        },
    }

if binary_political_interest:
    question_and_answer['political_interest'] = {
        "template": "Level of political interest: XXX",
        "valmap": {
            1: "Interested.",
            2: "Not interested."
        },
    }

if binary_political_interest:
    pi_2012 = pd.read_csv('short_binary_political_interest_0.csv')
else:
    pi_2012 = pd.read_csv('short_2.csv')

short_2012_political_interest_train, short_2012_political_interest_test = train_test_split(
    pi_2012, test_size=0.85, random_state=7, stratify=pi_2012["political_interest"])

class PoliticalInterest2012Signature(dspy.Signature):
    context = InputField(desc="ANES 2012 respondent's demographic and characteristics")

    age = InputField(desc="Respondent's age")
    campaign_interest = InputField(desc="Interest in political campaigns")
    voting_duty = InputField(desc="Sense of duty or choice in voting")
    ideology = InputField(desc="Political ideology")
    family_num = InputField(desc="Number of cohabiting family members")
    health = InputField(desc="Health status")
    life_satisfaction = InputField(desc="Life satisfaction")
    discuss_politics = InputField(desc="Whether discusses politics with family and friends")
    finance_past = InputField(desc="Present financial situation relative to the past")
    immigration_policy = InputField(desc="Attitude towards illegal immigrants")
    prediction = OutputField(desc="Predicted interest in politics: must be one of '1', '2', '3', or '4' (1=Very interested, 2=Somewhat interested, 3=Not very interested, 4=Not at all interested)")

if binary_political_interest:
  class PoliticalInterest2012Signature(dspy.Signature):
    context = InputField(desc="ANES 2012 respondent's demographic and characteristics")

    campaign_interest = InputField(desc="Interest in political campaigns")
    age = InputField(desc="Respondent's age")
    discuss_politics = InputField(desc="Whether discusses politics with family and friends")
    voting_duty = InputField(desc="Sense of duty or choice in voting")
    ideology = InputField(desc="Political ideology")
    family_num = InputField(desc="Number of cohabiting family members")
    health = InputField(desc="Health status")
    trust = InputField(desc="Level of trust in other people")
    life_satisfaction = InputField(desc="Life satisfaction")
    election_impact = InputField(desc="Effectiveness of elections as a mechanism for holding governments accountable")

    prediction = OutputField(desc="Predicted interest in politics: must be one of '1' or '2' (1=Interested, 2=Not interested)")

def map_val(q, val):
    q_meta = question_and_answer[q]
    return q_meta["valmap"].get(val, str(val))

train_set = []
if binary_political_interest:
  for _, row in short_2012_political_interest_train.iterrows():
     example = dspy.Example(
        context="2012 ANES respondent",
        campaign_interest=map_val("campaign_interest", row["campaign_interest"]),
        age=f"{int(row['age'])} years old.",
        discuss_politics=map_val("discuss_politics", row["discuss_politics"]),
        voting_duty=map_val("voting_duty", row["voting_duty"]),
        ideology=map_val("ideology", row["ideology"]),
        family_num=map_val("family_num", row["family_num"]),
        health=map_val("health", row["health"]),
        trust=map_val("trust", row["trust"]),
        life_satisfaction=map_val("life_satisfaction", row["life_satisfaction"]),
        election_impact=map_val("election_impact", row["election_impact"]),
        prediction=str(int(row["political_interest"]))
    ).with_inputs(
        "context",
        "campaign_interest",
        "age",
        "discuss_politics",
        "voting_duty",
        "ideology",
        "family_num",
        "health",
        "trust",
        "life_satisfaction",
        "election_impact",
    )

     train_set.append(example)

else:
    for _, row in short_2012_political_interest_train.iterrows():
        example = dspy.Example(
            context="2012 ANES respondent",
            age=f"{int(row['age'])} years old.",
            campaign_interest=map_val("campaign_interest", row["campaign_interest"]),
            voting_duty=map_val("voting_duty", row["voting_duty"]),
            ideology=map_val("ideology", row["ideology"]),
            family_num=map_val("family_num", row["family_num"]),
            health=map_val("health", row["health"]),
            life_satisfaction=map_val("life_satisfaction", row["life_satisfaction"]),
            discuss_politics=map_val("discuss_politics", row["discuss_politics"]),
            finance_past=map_val("finance_past", row["finance_past"]),
            immigration_policy=map_val("immigration_policy", row["immigration_policy"]),
            prediction=str(int(row["political_interest"]))
        ).with_inputs(
            "context",
            "age",
            "campaign_interest",
            "voting_duty",
            "ideology",
            "family_num",
            "health",
            "life_satisfaction",
            "discuss_politics",
            "finance_past",
            "immigration_policy"
        )

        train_set.append(example)

train_set[:2]

from dspy.teleprompt import BootstrapFewShotWithRandomSearch
from dspy.teleprompt import MIPROv2
from sklearn.metrics import f1_score
from tqdm import tqdm
import numpy as np

class PoliticalInterestPredictor(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(
            PoliticalInterest2012Signature
        )
    def forward(self, **kwargs):
        return self.predict(**kwargs)

'''
class PoliticalInterestPredictor(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.ChainOfThought(
            PoliticalInterest2012Signature
        )
    def forward(self, **kwargs):
        return self.predict(**kwargs)
'''

'''
def metric(example, prediction, trace=None):
    predicted = prediction.prediction
    # Validate prediction
    if predicted not in ["1", "2"]:
        return 0.0
    # Compute weighted F1-score for a single example
    return f1_score([example.prediction], [predicted], average="weighted", labels=["1", "2"])
'''
def metric(example, prediction, trace=None):
  predicted = prediction.prediction
  if binary_political_interest:
        valid_labels = ["1", "2"]
  else:
        valid_labels = ["1", "2", "3", "4"]

  if predicted not in valid_labels:
      print(f"Invalid prediction: {predicted} for example: {example}")
      return 10.0  # penalty for invalid

  true_label = int(example.prediction)
  pred_label = int(predicted)

  mae = abs(true_label - pred_label)
  return -mae

'''
optimizer = BootstrapFewShotWithRandomSearch(
    metric=metric,
    num_candidate_programs=8,  # Number of candidate prompt sets
    num_threads=4,  # Parallel threads for optimization
    max_bootstrapped_demos=4,  # Max few-shot examples
    max_labeled_demos=4  # Max labeled examples
)
'''
optimizer = MIPROv2(
    metric=metric,
    num_threads=4,
    max_labeled_demos=4,
)

model = PoliticalInterestPredictor()
compiled_model = optimizer.compile(model,
                                   trainset=train_set,
                                   requires_permission_to_run = False)

if binary_political_interest:
  compiled_model.save("political_interest_2012_binary_mipro.json")
  compiled_model.save("political_interest_2012_binary_mipro.pkl")
else:
  compiled_model.save("political_interest_2012_mipro.json")
  compiled_model.save("political_interest_2012_mipro.pkl")

test_set = []
if binary_political_interest:
  for _, row in short_2012_political_interest_test.iterrows():
     example = dspy.Example(
        context="2012 ANES respondent",
        campaign_interest=map_val("campaign_interest", row["campaign_interest"]),
        age=f"{int(row['age'])} years old.",
        discuss_politics=map_val("discuss_politics", row["discuss_politics"]),
        voting_duty=map_val("voting_duty", row["voting_duty"]),
        ideology=map_val("ideology", row["ideology"]),
        family_num=map_val("family_num", row["family_num"]),
        health=map_val("health", row["health"]),
        trust=map_val("trust", row["trust"]),
        life_satisfaction=map_val("life_satisfaction", row["life_satisfaction"]),
        election_impact=map_val("election_impact", row["election_impact"]),
        prediction=str(int(row["political_interest"]))
    ).with_inputs(
        "context",
        "campaign_interest",
        "age",
        "discuss_politics",
        "voting_duty",
        "ideology",
        "family_num",
        "health",
        "trust",
        "life_satisfaction",
        "election_impact",
    )

     test_set.append(example)

else:
    for _, row in short_2012_political_interest_test.iterrows():
        example = dspy.Example(
            context="2012 ANES respondent",
            age=f"{int(row['age'])} years old.",
            campaign_interest=map_val("campaign_interest", row["campaign_interest"]),
            voting_duty=map_val("voting_duty", row["voting_duty"]),
            ideology=map_val("ideology", row["ideology"]),
            family_num=map_val("family_num", row["family_num"]),
            health=map_val("health", row["health"]),
            life_satisfaction=map_val("life_satisfaction", row["life_satisfaction"]),
            discuss_politics=map_val("discuss_politics", row["discuss_politics"]),
            finance_past=map_val("finance_past", row["finance_past"]),
            immigration_policy=map_val("immigration_policy", row["immigration_policy"]),
            prediction=str(int(row["political_interest"]))
        ).with_inputs(
            "context",
            "age",
            "campaign_interest",
            "voting_duty",
            "ideology",
            "family_num",
            "health",
            "life_satisfaction",
            "discuss_politics",
            "finance_past",
            "immigration_policy"
        )

        test_set.append(example)

test_set[:2]

predictions = []
for example in tqdm(test_set, desc="Predicting"):
    pred = compiled_model(**example.inputs())
    predictions.append(pred.prediction)

short_2012_political_interest_test['dspy_prediction'] =  predictions

if binary_political_interest:
  short_2012_political_interest_test.to_csv('dspy_prediction_binary_2012.csv')
else:
  short_2012_political_interest_test.to_csv('dspy_prediction_2012.csv')

if binary_political_interest:
    pi_2016 = pd.read_csv('short_binary_political_interest_1.csv')
else:
    pi_2016 = pd.read_csv('short_5.csv')

short_2016_political_interest_train, short_2016_political_interest_test = train_test_split(
    pi_2016, test_size=0.85, random_state=2025, stratify=pi_2016["political_interest"])

class PoliticalInterest2016Signature(dspy.Signature):
    context = InputField(desc="ANES 2016 respondent's demographic and characteristics")

    age = InputField(desc="Respondent's age")
    campaign_interest = InputField(desc="Interest in political campaigns")
    voting_duty = InputField(desc="Sense of duty or choice in voting")
    ideology = InputField(desc="Political ideology")
    family_num = InputField(desc="Number of cohabiting family members")
    health = InputField(desc="Health status")
    life_satisfaction = InputField(desc="Life satisfaction")
    finance_past = InputField(desc="Present financial situation relative to the past")
    finance_next = InputField(desc="Expected future financial situation relative to the present")
    trust = InputField(desc="Level of trust in other people")

    prediction = OutputField(desc="Predicted interest in politics: must be one of '1', '2', '3', or '4' (1=Very interested, 2=Somewhat interested, 3=Not very interested, 4=Not at all interested)")

if binary_political_interest:
  class PoliticalInterest2016Signature(dspy.Signature):
    context = InputField(desc="ANES 2016 respondent's demographic and characteristics")

    campaign_interest = InputField(desc="Interest in political campaigns")
    age = InputField(desc="Respondent's age")
    discuss_politics = InputField(desc="Whether discusses politics with family and friends")
    voting_duty = InputField(desc="Sense of duty or choice in voting")
    ideology = InputField(desc="Political ideology")
    family_num = InputField(desc="Number of cohabiting family members")
    health = InputField(desc="Health status")
    life_satisfaction = InputField(desc="Life satisfaction")
    trust = InputField(desc="Level of trust in other people")
    finance_past = InputField(desc="Present financial situation relative to the past")

    prediction = OutputField(desc="Predicted interest in politics: must be one of '1' or '2' (1=Interested, 2=Not interested)")

train_set = []
if binary_political_interest:
  for _, row in short_2016_political_interest_train.iterrows():
     example = dspy.Example(
        context="2016 ANES respondent",
        campaign_interest=map_val("campaign_interest", row["campaign_interest"]),
        age=f"{int(row['age'])} years old.",
        discuss_politics=map_val("discuss_politics", row["discuss_politics"]),
        voting_duty=map_val("voting_duty", row["voting_duty"]),
        ideology=map_val("ideology", row["ideology"]),
        family_num=map_val("family_num", row["family_num"]),
        health=map_val("health", row["health"]),
        life_satisfaction=map_val("life_satisfaction", row["life_satisfaction"]),
        trust=map_val("trust", row["trust"]),
        finance_past=map_val("finance_past", row["finance_past"]),
        prediction=str(int(row["political_interest"]))
    ).with_inputs(
        "context",
        "campaign_interest",
        "age",
        "discuss_politics",
        "voting_duty",
        "ideology",
        "family_num",
        "health",
        "life_satisfaction",
        "trust",
        "finance_past",
    )

     train_set.append(example)

else:
  for _, row in short_2016_political_interest_train.iterrows():
    example = dspy.Example(
        context="2016 ANES respondent",
        age=f"{int(row['age'])} years old",
        campaign_interest=map_val("campaign_interest", row["campaign_interest"]),
        voting_duty=map_val("voting_duty", row["voting_duty"]),
        ideology=map_val("ideology", row["ideology"]),
        family_num=map_val("family_num", row["family_num"]),
        health=map_val("health", row["health"]),
        life_satisfaction=map_val("life_satisfaction", row["life_satisfaction"]),
        finance_past=map_val("finance_past", row["finance_past"]),
        finance_next=map_val("finance_next", row["finance_next"]),
        trust=map_val("trust", row["trust"]),
        prediction=str(int(row["political_interest"]))
    ).with_inputs(
        "context",
        "age",
        "campaign_interest",
        "voting_duty",
        "ideology",
        "family_num",
        "health",
        "life_satisfaction",
        "finance_past",
        "finance_next",
        "trust"
    )
    train_set.append(example)

train_set[:2]

class PoliticalInterestPredictor(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(
            PoliticalInterest2016Signature
        )
    def forward(self, **kwargs):
        return self.predict(**kwargs)

model = PoliticalInterestPredictor()
compiled_model_2016 = optimizer.compile(model,
                                        trainset=train_set,
                                        requires_permission_to_run = False)

if binary_political_interest:
  compiled_model_2016.save("political_interest_2016_binary_mipro.json")
  compiled_model_2016.save("political_interest_2016_binary_mipro.pkl")
else:
  compiled_model_2016.save("political_interest_2016_mipro.json")
  compiled_model_2016.save("political_interest_2016_mipro.pkl")

test_set = []
if binary_political_interest:
  for _, row in short_2016_political_interest_test.iterrows():
     example = dspy.Example(
        context="2016 ANES respondent",
        campaign_interest=map_val("campaign_interest", row["campaign_interest"]),
        age=f"{int(row['age'])} years old.",
        discuss_politics=map_val("discuss_politics", row["discuss_politics"]),
        voting_duty=map_val("voting_duty", row["voting_duty"]),
        ideology=map_val("ideology", row["ideology"]),
        family_num=map_val("family_num", row["family_num"]),
        health=map_val("health", row["health"]),
        life_satisfaction=map_val("life_satisfaction", row["life_satisfaction"]),
        trust=map_val("trust", row["trust"]),
        finance_past=map_val("finance_past", row["finance_past"]),
        prediction=str(int(row["political_interest"]))
    ).with_inputs(
        "context",
        "campaign_interest",
        "age",
        "discuss_politics",
        "voting_duty",
        "ideology",
        "family_num",
        "health",
        "life_satisfaction",
        "trust",
        "finance_past",
    )

     test_set.append(example)

else:
  for _, row in short_2016_political_interest_test.iterrows():
    example = dspy.Example(
        context="2016 ANES respondent",
        age=f"{int(row['age'])} years old",
        campaign_interest=map_val("campaign_interest", row["campaign_interest"]),
        voting_duty=map_val("voting_duty", row["voting_duty"]),
        ideology=map_val("ideology", row["ideology"]),
        family_num=map_val("family_num", row["family_num"]),
        health=map_val("health", row["health"]),
        life_satisfaction=map_val("life_satisfaction", row["life_satisfaction"]),
        finance_past=map_val("finance_past", row["finance_past"]),
        finance_next=map_val("finance_next", row["finance_next"]),
        trust=map_val("trust", row["trust"]),
        prediction=str(int(row["political_interest"]))
    ).with_inputs(
        "context",
        "age",
        "campaign_interest",
        "voting_duty",
        "ideology",
        "family_num",
        "health",
        "life_satisfaction",
        "finance_past",
        "finance_next",
        "trust"
    )
    test_set.append(example)

test_set[:2]

predictions_2016 = []

for example in tqdm(test_set, desc="Predicting"):
    pred = compiled_model_2016(**example.inputs())
    predictions_2016.append(pred.prediction)

short_2016_political_interest_test['dspy_prediction'] =  predictions_2016

if binary_political_interest:
  short_2016_political_interest_test.to_csv('dspy_prediction_binary_2016.csv')
else:
  short_2016_political_interest_test.to_csv('dspy_prediction_2016.csv')

if binary_political_interest:
    pi_2020 = pd.read_csv('short_binary_political_interest_2.csv')
else:
    pi_2020 = pd.read_csv('short_8.csv')

short_2020_political_interest_train, short_2020_political_interest_test = train_test_split(
    pi_2020, test_size=0.85, random_state=9, stratify=pi_2020["political_interest"])

class PoliticalInterest2020Signature(dspy.Signature):
    context = InputField(desc="ANES 2020 respondent's demographic and characteristics")

    age = InputField(desc="Respondent's age")
    campaign_interest = InputField(desc="Interest in political campaigns")
    ideology = InputField(desc="Political ideology")
    voting_duty = InputField(desc="Sense of duty or choice in voting")
    family_num = InputField(desc="Number of cohabiting family members")
    health = InputField(desc="Health status")
    finance_past = InputField(desc="Present financial situation relative to the past")
    life_satisfaction = InputField(desc="Life satisfaction")
    trust = InputField(desc="Level of trust in other people")
    finance_next = InputField(desc="Expected future financial situation relative to the present")

    prediction = OutputField(desc="Predicted interest in politics: must be one of '1', '2', '3', or '4' (1=Very interested, 2=Somewhat interested, 3=Not very interested, 4=Not at all interested)")

if binary_political_interest:
  class PoliticalInterest2020Signature(dspy.Signature):
    context = InputField(desc="ANES 2020 respondent's demographic and characteristics")

    campaign_interest = InputField(desc="Interest in political campaigns")
    age = InputField(desc="Respondent's age")
    voting_duty = InputField(desc="Sense of duty or choice in voting")
    ideology = InputField(desc="Political ideology")
    family_num = InputField(desc="Number of cohabiting family members")
    health = InputField(desc="Health status")
    finance_past = InputField(desc="Present financial situation relative to the past")
    life_satisfaction = InputField(desc="Life satisfaction")
    trust = InputField(desc="Level of trust in other people")
    election_impact = InputField(desc="Effectiveness of elections as a mechanism for holding governments accountable")

    prediction = OutputField(desc="Predicted interest in politics: must be one of '1' or '2' (1=Interested, 2=Not interested)")

short_2020_political_interest_train[:2]

train_set = []
if binary_political_interest:
  for _, row in short_2020_political_interest_train.iterrows():
     example = dspy.Example(
        context="2020 ANES respondent",
        campaign_interest=map_val("campaign_interest", row["campaign_interest"]),
        age=f"{int(row['age'])} years old.",
        voting_duty=map_val("voting_duty", row["voting_duty"]),
        ideology=map_val("ideology", row["ideology"]),
        family_num=map_val("family_num", row["family_num"]),
        health=map_val("health", row["health"]),
        finance_past=map_val("finance_past", row["finance_past"]),
        life_satisfaction=map_val("life_satisfaction", row["life_satisfaction"]),
        trust=map_val("trust", row["trust"]),
        election_impact=map_val("election_impact", row["election_impact"]),
        prediction=str(int(row["political_interest"]))
    ).with_inputs(
        "context",
        "campaign_interest",
        "age",
        "voting_duty",
        "ideology",
        "family_num",
        "health",
        "finance_past",
        "life_satisfaction",
        "trust",
        "election_impact"
    )

     train_set.append(example)

else:
  for _, row in short_2020_political_interest_train.iterrows():
    example = dspy.Example(
        context="2020 ANES respondent",
        age=f"{int(row['age'])} years old",
        campaign_interest=map_val("campaign_interest", row["campaign_interest"]),
        ideology=map_val("ideology", row["ideology"]),
        voting_duty=map_val("voting_duty", row["voting_duty"]),
        family_num=map_val("family_num", row["family_num"]),
        health=map_val("health", row["health"]),
        finance_past=map_val("finance_past", row["finance_past"]),
        life_satisfaction=map_val("life_satisfaction", row["life_satisfaction"]),
        trust=map_val("trust", row["trust"]),
        finance_next=map_val("finance_next", row["finance_next"]),
        prediction=str(int(row["political_interest"]))
    ).with_inputs(
        "context",
        "age",
        "campaign_interest",
        "voting_duty",
        "ideology",
        "family_num",
        "health",
        "finance_past",
        "life_satisfaction",
        "trust",
        "finance_next"
    )
    train_set.append(example)

train_set[:2]

class PoliticalInterestPredictor(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(
            PoliticalInterest2020Signature
        )
    def forward(self, **kwargs):
        return self.predict(**kwargs)

model = PoliticalInterestPredictor()
compiled_model_2020 = optimizer.compile(model, trainset=train_set,
                                        requires_permission_to_run = False)

if binary_political_interest:
  compiled_model_2020.save("political_interest_2020_binary_mipro.json")
  compiled_model_2020.save("political_interest_2020_binary_mipro.pkl")
else:
  compiled_model_2020.save("political_interest_2020_mipro.json")
  compiled_model_2020.save("political_interest_2020_mipro.pkl")

test_set = []
if binary_political_interest:
    for _, row in short_2020_political_interest_test.iterrows():
        example = dspy.Example(
            context="2020 ANES respondent",
            campaign_interest=map_val("campaign_interest", row["campaign_interest"]),
            age=f"{int(row['age'])} years old.",
            voting_duty=map_val("voting_duty", row["voting_duty"]),
            ideology=map_val("ideology", row["ideology"]),
            family_num=map_val("family_num", row["family_num"]),
            health=map_val("health", row["health"]),
            finance_past=map_val("finance_past", row["finance_past"]),
            life_satisfaction=map_val("life_satisfaction", row["life_satisfaction"]),
            trust=map_val("trust", row["trust"]),
            election_impact=map_val("election_impact", row["election_impact"]),
            prediction=str(int(row["political_interest"]))
        ).with_inputs(
            "context",
            "campaign_interest",
            "age",
            "voting_duty",
            "ideology",
            "family_num",
            "health",
            "finance_past",
            "life_satisfaction",
            "trust",
            "election_impact"
        )
        test_set.append(example)

else:
    for _, row in short_2020_political_interest_test.iterrows():
        example = dspy.Example(
            context="2020 ANES respondent",
            age=f"{int(row['age'])} years old",
            campaign_interest=map_val("campaign_interest", row["campaign_interest"]),
            voting_duty=map_val("voting_duty", row["voting_duty"]),
            ideology=map_val("ideology", row["ideology"]),
            family_num=map_val("family_num", row["family_num"]),
            health=map_val("health", row["health"]),
            finance_past=map_val("finance_past", row["finance_past"]),
            life_satisfaction=map_val("life_satisfaction", row["life_satisfaction"]),
            trust=map_val("trust", row["trust"]),
            finance_next=map_val("finance_next", row["finance_next"]),
            prediction=str(int(row["political_interest"]))
        ).with_inputs(
            "context",
            "age",
            "campaign_interest",
            "voting_duty",
            "ideology",
            "family_num",
            "health",
            "finance_past",
            "life_satisfaction",
            "trust",
            "finance_next"
        )
        test_set.append(example)
test_set[:2]

predictions_2020 = []
for example in tqdm(test_set, desc="Predicting"):
    pred = compiled_model_2020(**example.inputs())
    predictions_2020.append(pred.prediction)

short_2020_political_interest_test['dspy_prediction'] =  predictions_2020
if binary_political_interest:
  short_2020_political_interest_test.to_csv('dspy_prediction_binary_2020.csv')
else:
  short_2020_political_interest_test.to_csv('dspy_prediction_2020.csv')

