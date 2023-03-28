# ultimatum_robot_responder: offer (X or Y)
# ultimatum_robot_proposer: accept_x (bool), accept_y (bool)
# trust_robot_secondmover: trust (bool)
# trust_robot_firstmover: decision if trusted (X or Y)

#%%
import pandas as pd
import random
import statistics
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_fscore_support


#%%
def make_prediction(data_file, input_values, seed=None, trees=10):

    # set seed for multiple predictions
    if seed is not None:
        random.seed(seed)

    # import and split data
    data = pd.read_csv(data_file)
    cols = data.shape[1]
    train = sorted(random.sample(population=range(data.shape[0]), k=int(0.8*data.shape[0])))
    test = [x for x in range(data.shape[0]) if x not in train]
    data_train = data.iloc[train, :]
    data_test = data.iloc[test, :]
    inputs_train = data_train.iloc[:, range(cols - 1)]
    inputs_test = data_test.iloc[:, range(cols - 1)]
    output_train = data_train.iloc[:, cols - 1]
    output_test = data_test.iloc[:, cols - 1]

    # Draw "artificial human"
    avg_age = statistics.mean(data["age"])
    sd_age = statistics.stdev(data["age"])
    age = round(random.gauss(mu=avg_age, sigma=sd_age))
    while age < 18:
        age = round(random.gauss(mu=avg_age, sigma=sd_age))

    weights_degree = data["degree"].value_counts(normalize=True)
    weights_degree = weights_degree.sort_index()
    degree = random.choices(weights_degree.index, weights=weights_degree)[0]

    weights_familiarity = data["familiarity"].value_counts(normalize=True)
    weights_familiarity = weights_familiarity.sort_index()
    familiarity = random.choices(weights_familiarity.index, weights=weights_familiarity)[0]

    weights_confidence = data["confidence"].value_counts(normalize=True)
    weights_confidence = weights_confidence.sort_index()
    confidence = random.choices(weights_confidence.index, weights=weights_confidence)[0]

    weights_redistribution = data["redistribution"].value_counts(normalize=True)
    weights_redistribution = weights_redistribution.sort_index()
    redistribution = random.choices(weights_redistribution.index, weights=weights_redistribution)[0]

    weights_gender = [statistics.mean(data.iloc[:, i]) for i in range(5, 8)]
    gender = random.choices(range(3), weights=weights_gender)[0]
    gender_vec = [0] * 3
    gender_vec[gender] = 1

    weights_study = [statistics.mean(data.iloc[:, i]) for i in range(8, 18)]
    study = random.choices(range(10), weights=weights_study)[0]
    study_vec = [0] * 10
    study_vec[study] = 1

    weights_employment = [statistics.mean(data.iloc[:, i]) for i in range(18, 21)]
    employment = random.choices(range(3), weights=weights_employment)[0]
    employment_vec = [0] * 3
    employment_vec[employment] = 1

    # initialize classifier
    rf_clf = RandomForestClassifier(n_estimators=trees, random_state=123)

    # new dataframe for prediction
    data_new = pd.DataFrame(columns=inputs_train.columns)
    for row in range(len(input_values)):
        new_row = [age, degree, familiarity, confidence, redistribution] + gender_vec + study_vec + employment_vec + input_values[row]
        data_new.loc[row] = new_row

    # build RF
    rf_clf = rf_clf.fit(inputs_train, output_train)

    # train-test accuracy
    accuracy = rf_clf.score(inputs_test, output_test)
    prediction_for_score = rf_clf.predict(inputs_test)
    scores = precision_recall_fscore_support(y_true=output_test, y_pred=prediction_for_score, average="binary")

    # out-of-sample prediction
    prediction_new = rf_clf.predict(data_new)

    return dict(
        accuracy=accuracy,
        scores=scores,
        prediction=prediction_new
    )


def make_full_predictions(data_file, input_values, num_participants, trees=None, seed_multiplier=123):

    # initialize empty dataset
    columns = ["prediction_" + str(t) for t in range(1, 31)]
    predictions = pd.DataFrame(columns=columns)
    accuracy = []
    precision = []
    recall = []
    f1 = []
    print(data_file)

    # predict for each participant
    for participant in range(num_participants):
        if trees is None:
            prediction = make_prediction(data_file=data_file,
                                         input_values=input_values,
                                         seed=seed_multiplier * (participant + 1))
        else:
            prediction = make_prediction(data_file=data_file,
                                         input_values=input_values,
                                         seed=seed_multiplier * (participant + 1),
                                         trees=trees)
        new_row = list(prediction["prediction"])
        predictions.loc[participant] = new_row
        accuracy.append(prediction["accuracy"])
        precision.append(prediction["scores"][0])
        recall.append(prediction["scores"][1])
        f1.append(prediction["scores"][2])
        print(str(participant + 1) + " of " + str(num_participants))

    return dict(
        accuracy=statistics.mean(accuracy),
        precision=statistics.mean(precision),
        recall=statistics.mean(recall),
        f1_score=statistics.mean(f1),
        predictions=predictions
    )


self_x = [330, 350, 370, 390, 400, 440, 450, 470, 510, 520,
          600, 620, 640, 660, 670, 710, 720, 740, 780, 790,
          870, 890, 910, 930, 940, 980, 990, 1010, 1050, 1060]
other_x = [680, 680, 680, 1050, 690, 710, 1020, 730, 810, 870,
           410, 410, 410, 780, 420, 440, 750, 460, 540, 600,
           140, 140, 140, 510, 150, 170, 480, 190, 270, 330]
self_y = [330, 310, 290, 270, 260, 220, 210, 190, 150, 140,
          600, 580, 560, 540, 530, 490, 480, 460, 420, 410,
          870, 850, 830, 810, 800, 760, 750, 730, 690, 680]
other_y = [1060, 1060, 1060, 690, 1050, 1030, 720, 1010, 930, 870,
           790, 790, 790, 420, 780, 760, 450, 740, 660, 600,
           520, 520, 520, 150, 510, 490, 180, 470, 390, 330]

self_z_wel = [190, 170, 150, 130, 120, 80, 70, 50, 10, 0,
              460, 440, 420, 400, 390, 350, 340, 320, 280, 270,
              730, 710, 690, 670, 660, 620, 610, 590, 550, 540]
other_z_wel = [1200, 1200, 1200, 830, 1190, 1170, 860, 1150, 1070, 1010,
               930, 930, 930, 560, 920, 900, 590, 880, 800, 740,
               660, 660, 660, 290, 650, 630, 320, 610, 530, 470]
self_z_mis = [470, 490, 510, 530, 540, 580, 590, 610, 650, 660,
              740, 760, 780, 800, 810, 850, 860, 880, 920, 930,
              1010, 1030, 1050, 1070, 1080, 1120, 1130, 1150, 1190, 1200]
other_z_mis = [540, 540, 540, 910, 550, 570, 880, 590, 670, 730,
               270, 270, 270, 640, 280, 300, 610, 320, 400, 460,
               0, 0, 0, 370, 10, 30, 340, 50, 130, 190]

data_trust_first_wel = "trust_robot_secondmover/data_trust_first_wel.csv"
data_trust_first_mis = "trust_robot_secondmover/data_trust_first_mis.csv"
input_values_trust_wel = [[self_x[i], self_y[i], self_z_wel[i], other_x[i], other_y[i], other_z_wel[i]] for i in range(30)]
input_values_trust_mis = [[self_x[i], self_y[i], self_z_mis[i], other_x[i], other_y[i], other_z_mis[i]] for i in range(30)]


#%%
predictions_trust_first_wel = make_full_predictions(data_file=data_trust_first_wel,
                                                    input_values=input_values_trust_wel,
                                                    num_participants=1000,
                                                    trees=100,
                                                    seed_multiplier=123)
predictions_trust_first_mis = make_full_predictions(data_file=data_trust_first_mis,
                                                    input_values=input_values_trust_mis,
                                                    num_participants=1000,
                                                    trees=100,
                                                    seed_multiplier=123)

print("Accuracy Wel:  " + str(predictions_trust_first_wel["accuracy"]))
print("Precision Wel: " + str(predictions_trust_first_wel["precision"]))
print("Recall Wel:    " + str(predictions_trust_first_wel["recall"]))
print("F1 Score Wel:  " + str(predictions_trust_first_wel["f1_score"]))
print("")
print("Accuracy Mis:  " + str(predictions_trust_first_mis["accuracy"]))
print("Precision Mis: " + str(predictions_trust_first_mis["precision"]))
print("Recall Mis:    " + str(predictions_trust_first_mis["recall"]))
print("F1 Score Mis:  " + str(predictions_trust_first_mis["f1_score"]))
print("")
print("Accuracy:  " + str((predictions_trust_first_wel["accuracy"] + predictions_trust_first_mis["accuracy"])/2))
print("Precision: " + str((predictions_trust_first_wel["precision"] + predictions_trust_first_mis["precision"])/2))
print("Recall:    " + str((predictions_trust_first_wel["recall"] + predictions_trust_first_mis["recall"])/2))
print("F1 Score:  " + str((predictions_trust_first_wel["f1_score"] + predictions_trust_first_mis["f1_score"])/2))

#%%

predictions_trust_first_wel["predictions"].to_csv(
    path_or_buf="trust_robot_secondmover/predictions_trust_first_wel.csv",
    index=False
)
predictions_trust_first_mis["predictions"].to_csv(
    path_or_buf="trust_robot_secondmover/predictions_trust_first_mis.csv",
    index=False
)
