import pytest
from src.manager import Manager
from src.models import Parameters, Bill, Apartment, ApartmentSettlement

def test_create_apartment_settlement_logic():
  
    params = Parameters()
    manager = Manager(params)
    
    manager.apartments['test-apt'] = Apartment(
        key='test-apt', name='Test Apt', location='City', area_m2=50.0, rooms={})
    
    
    manager.bills = [
        Bill(apartment='test-apt', amount_pln=100.0, date_due='2026-01-10', 
             settlement_year=2026, settlement_month=1, type='electricity'),
        Bill(apartment='test-apt', amount_pln=250.0, date_due='2026-01-15', 
             settlement_year=2026, settlement_month=1, type='water'),
        Bill(apartment='other-apt', amount_pln=500.0, date_due='2026-01-15', 
             settlement_year=2026, settlement_month=1, type='rent')]
    
    settlement = manager.create_apartment_settlement('test-apt', 2026, 1)
    
    
    assert isinstance(settlement, ApartmentSettlement)
    assert settlement.apartment == 'test-apt'
    assert settlement.year == 2026
    assert settlement.month == 1
    assert settlement.total_bills_pln == 350.0  
    assert settlement.total_rent_pln == 0.0     
    assert settlement.total_due_pln == -350.0   


    settlement_empty = manager.create_apartment_settlement('test-apt', 2026, 2) 
    
    assert settlement_empty.apartment == 'test-apt'
    assert settlement_empty.total_bills_pln == 0.0
    assert settlement_empty.total_due_pln == 0.0
    assert settlement_empty.month == 2
    
    assert manager.create_apartment_settlement('non-existent', 2026, 1) is None