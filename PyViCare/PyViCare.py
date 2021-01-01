from PyViCare.PyViCareGazBoiler import GazBoiler

def readFeature(entities, property_name):
    feature = next((f for f in entities if f["class"][0] == property_name and f["class"][1] == "feature"), {})
    return feature

# DEPRECATED
class ViCareSession(GazBoiler):
    def dummy(self):
        print("done")

