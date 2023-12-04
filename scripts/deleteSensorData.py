from tof.models import IncidentData, LdrData, VizData, TofData2, TofData1, TofData, VehicleInfo

def retain_max_records(model, max_records=0):
    """Retain only the maximum specified number of records for a given model."""
    count = model.objects.count()
    if count > max_records:
        # Fetch the IDs of the oldest records that exceed the max_records limit
        ids_to_delete = model.objects.all().order_by('id')[max_records:].values_list('id', flat=True)
        # Delete these records
        model.objects.filter(id__in=ids_to_delete).delete()
        print(f"Deleted {count - max_records} records from {model.__name__}")


def run():
    # Call the function for each model
    retain_max_records(IncidentData)
    retain_max_records(LdrData)
    retain_max_records(VizData)
    retain_max_records(TofData2)
    retain_max_records(TofData1)
    retain_max_records(TofData)
    retain_max_records(VehicleInfo)

    print("Operation completed.")