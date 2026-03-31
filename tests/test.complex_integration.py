from src.models import Parameters, Bill, Apartment
from src.manager import Manager 

def test_get_apartment_costs(monkeypatch):
    parameters = Parameters()
    manager = Manager(parameters)

    manager.apartments = {'A1': Apartment(key='A1', name='Apartment 1', location='City Center', area_m2=50, rooms={}),
                          'A2': Apartment(key='A2', name='Apartment 2', location='City Center', area_m2=50, rooms={})}
    
    manager.bills = [Bill(apartment='A1', amount_pln=150, date_due='2024-03-05', settlement_year=2024, settlement_month=3, type='water'),
                     Bill(apartment='A1', amount_pln=100, date_due='2024-03-10', settlement_year=2024, settlement_month=3, type='electricity'),
                     Bill(apartment='A2', amount_pln=200, date_due='2024-04-01', settlement_year=2024, settlement_month=4, type='gas'),
                     Bill(apartment='A2', amount_pln=300, date_due='2024-03-15', settlement_year=2024, settlement_month=3, type='water')]
    
    assert manager.get_apartment_costs('A666',2024, 3) == 0 
    assert manager.get_apartment_costs('A1',2024, 4) == 0 
    assert manager.get_apartment_costs('A1',2024,3) == 250 