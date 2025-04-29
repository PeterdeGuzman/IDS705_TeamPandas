#Loading final merged dataset
restaurants = pd.read_csv("/Users/pdeguz01/Documents/git/Data/IDS705_Final/Working Dataset/MOST RECENT DATA/restauranthealthinspections2024_CensusSVIUSDA_halfmileradius.csv")


# encoding datetime information before training model
restaurants["INSPECTION_DATE"] = restaurants["INSPECTION_DATE"].astype("datetime64[ns]")
restaurants["INSPDATE_MONTH"] = restaurants["INSPECTION_DATE"].dt.month
restaurants["INSPDATE_DAY"] = restaurants["INSPECTION_DATE"].dt.day


restaurants = restaurants[
    ~restaurants["STORE_NAME"].str.contains("SCHOOL", case=False, na=False)
]


CA_restaurants = restaurants[restaurants["State"] == "CA"]
CA_restaurants = CA_restaurants.dropna(thresh=(int(len(CA_restaurants) * 0.15)), axis=1)
CA_restaurants = CA_restaurants.dropna()

CA_restaurants = CA_restaurants.drop(columns=["EP_POV150"])


# pulling 20% of this dataset for our test
CA_restaurant_test = CA_restaurants.sample(frac=0.2, random_state=42)
# drop these 20% pulled from our training set
CA_restaurants = CA_restaurants.drop(CA_restaurant_test.index)


CA_restaurant_model_grades = CA_restaurants[
    [
        "INSPDATE_YEAR",
        "INSPDATE_MONTH",
        "INSPDATE_DAY",
        "EP_UNEMP",
        "EP_HBURD",
        "EP_NOHSDP",
        "EP_UNINSUR",
        "EP_AGE65",
        "EP_AGE17",
        "EP_DISABL",
        "EP_SNGPNT",
        "EP_LIMENG",
        "EP_MINRTY",
        "EP_MUNIT",
        "EP_MOBILE",
        "EP_CROWD",
        "EP_NOVEH",
        "EP_GROUPQ",
        "USDA_PovertyRate",
        "USDA_MedianFamilyIncome",
        "USDA_PCTGQTRS",
        "GRADE",
    ]
]

# appending all columns with "share" in the column name
CA_share_cols = CA_restaurants[CA_restaurants.filter(like="share").columns]
CA_restaurant_model_grades = pd.concat(
    [CA_restaurant_model_grades, CA_share_cols],
    axis=1,
)
# resetting index
CA_restaurant_model_grades.reset_index(drop=True, inplace=True)

# X = restaurant_model_grades[[i for i in list(restaurant_model_grades.columns) if i != "GRADE"]]
X = CA_restaurant_model_grades.drop("GRADE", axis=1)
y = CA_restaurant_model_grades[["GRADE"]]

# encoding target labels (A, B, C -> 0, 1, 2)
target_label = LabelEncoder()
y_encoded = target_label.fit_transform(y)
# binarize labels/one-hot encoding (needed for one-vs-rest when calculating ROC/AUC and PR curve)
y_bin = label_binarize(y_encoded, classes=[0, 1, 2])
# num_classes = len(pd.unique(y["GRADE"]))
num_classes = y_bin.shape[1]

# train/test split
X_train_grade, X_test_grade, y_train_grade, y_test_grade = train_test_split(
    X, y_bin, test_size=0.3, random_state=42
)

# normalizing our data using our MinMaxScaler
# transforms each value in the col proportionally within [0,1]
scaler = MinMaxScaler()
X_train_grade_scaled = scaler.fit_transform(X_train_grade)
X_test_grade_scaled = scaler.fit_transform(X_test_grade)

LR = OneVsRestClassifier(
    LogisticRegression(
        max_iter=1000,
        multi_class="multinomial",
        penalty="l2",
        solver="lbfgs",
        class_weight="balanced",
    )
)

LR.fit(X_train_grade_scaled, y_train_grade)

LR_y_pred = LR.predict_proba(X_test_grade_scaled)



# plotting ROC for each class
fpr = dict()
tpr = dict()
roc_auc = dict()

# compute ROC curve and ROC area for each class
for i in range(num_classes):
    fpr[i], tpr[i], _ = roc_curve(y_test_grade[:, i], LR_y_pred[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

plt.figure(figsize=(8, 6))
# plot ROC curve for a specific class
for i in range(num_classes):
    plt.plot(fpr[i], tpr[i], label=f"Class {i} (AUC = {roc_auc[i]:.2f})")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve for Multinomial Logistic Regression")
plt.legend()
plt.show()


precision = dict()
recall = dict()
avg_precision = dict()

# plotting each PR curve
plt.figure(figsize=(8, 6))
for i in range(num_classes):
    precision[i], recall[i], _ = precision_recall_curve(
        y_test_grade[:, i], LR_y_pred[:, i]
    )
    avg_precision[i] = average_precision_score(y_test_grade[:, i], LR_y_pred[:, i])
    plt.plot(recall[i], precision[i], label=f"Class {i} (AP = {avg_precision[i]:.2f})")

plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Precision-Recall Curve - Multinomial Logistic Regression")
plt.legend()
plt.show()