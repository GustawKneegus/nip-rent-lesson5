import pytest
from src.manager import Manager
from src.models import Parameters, Apartment, Tenant, ApartmentSettlement, TenantSettlement

def test_create_tenant_settlements_logic():
    params = Parameters()
    manager = Manager(params)
    
    apt_key = 'apt-1'
    manager.apartments[apt_key] = Apartment(
        key=apt_key, name='Mieszkanie 1', location='Centrum', area_m2=50.0, rooms={})
    
    manager.tenants = {
        't1': Tenant(name='Jan', apartment=apt_key, room='r1', rent_pln=1000, deposit_pln=0, 
                     date_agreement_from='2024-01-01', date_agreement_to='2024-12-31'),
        't2': Tenant(name='Anna', apartment=apt_key, room='r2', rent_pln=1000, deposit_pln=0, 
                     date_agreement_from='2024-01-01', date_agreement_to='2024-12-31')}
    
    apt_settlement = ApartmentSettlement(
        apartment=apt_key, month=3, year=2024, total_rent_pln=0, total_bills_pln=600.0, total_due_pln=-600.0)
    
    tenant_settlements = manager.create_tenant_settlements(apt_settlement)
    
    assert len(tenant_settlements) == 2
    assert tenant_settlements[0].bills_pln == 300.0  # 600 / 2
    assert tenant_settlements[1].bills_pln == 300.0
    assert tenant_settlements[0].tenant in ['Jan', 'Anna']
    assert tenant_settlements[0].total_due_pln == -300.0


    manager.tenants = {
        't3': Tenant(name='Marek', apartment='apt-2', room='r1', rent_pln=1000, deposit_pln=0, 
                     date_agreement_from='2024-01-01', date_agreement_to='2024-12-31')
    }
    manager.apartments['apt-2'] = Apartment(key='apt-2', name='M2', location='X', area_m2=20, rooms={})
    apt_settlement_single = ApartmentSettlement(
        apartment='apt-2', month=3, year=2024, total_rent_pln=0, total_bills_pln=450.0, total_due_pln=-450.0
    )
    
    tenant_settlements_single = manager.create_tenant_settlements(apt_settlement_single)
    

    assert len(tenant_settlements_single) == 1
    assert tenant_settlements_single[0].tenant == 'Marek'
    assert tenant_settlements_single[0].bills_pln == 450.0


    apt_settlement_empty = ApartmentSettlement(
        apartment='apt-empty', month=3, year=2024, total_rent_pln=0, total_bills_pln=100.0, total_due_pln=-100.0
    )
    tenant_settlements_empty = manager.create_tenant_settlements(apt_settlement_empty)
    
    assert isinstance(tenant_settlements_empty, list)
    assert len(tenant_settlements_empty) == 0