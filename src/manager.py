from src.models import Apartment, Bill, Parameters, Tenant, Transfer, ApartmentSettlement, TenantSettlement


class Manager:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters 

        self.apartments = {}
        self.tenants = {}
        self.transfers = []
        self.bills = []
       
        self.load_data()

    def load_data(self):
        self.apartments = Apartment.from_json_file(self.parameters.apartments_json_path)
        self.tenants = Tenant.from_json_file(self.parameters.tenants_json_path)
        self.transfers = Transfer.from_json_file(self.parameters.transfers_json_path)
        self.bills = Bill.from_json_file(self.parameters.bills_json_path)

    def check_tenants_apartment_keys(self) -> bool:
        for tenant in self.tenants.values():
            if tenant.apartment not in self.apartments:
                return False
        return True
    
    def get_apartment_costs(self, apartment_key: str, year = None , month = None ) -> float | None:
        if apartment_key not in self.apartments:
            return None

        filtered_bills = [
            bill for bill in self.bills
            if bill.apartment == apartment_key
            and (year == 0 or bill.settlement_year == year or year is None)
        and (month == 0 or bill.settlement_month == month or month is None)
        ]

        if not filtered_bills:
            return 0.0

        total = sum(bill.amount_pln for bill in filtered_bills)
        return float(total)
   
    def create_apartment_settlement(self, apartment_key: str, year: int, month: int) -> ApartmentSettlement | None:
      
        if apartment_key not in self.apartments:
            return None

      
        total_bills = self.get_apartment_costs(apartment_key, year, month)
        
        bills_sum = float(total_bills) if total_bills is not None else 0.0
        
        total_rent = 0.0 
 
        total_due = total_rent - bills_sum

        return ApartmentSettlement(apartment=apartment_key,month=month,year=year,total_rent_pln=total_rent,total_bills_pln=bills_sum,
            total_due_pln=total_due)
        
    def create_tenant_settlements(self, apt_settlement: ApartmentSettlement) -> List[TenantSettlement]:
       
        active_tenants = [
            t for t in self.tenants.values() 
            if t.apartment == apt_settlement.apartment
        ]
        
        if not active_tenants:
            return []
            
        number_of_tenants = len(active_tenants)
        share_of_bills = apt_settlement.total_bills_pln / number_of_tenants
        
        settlements = []
        for tenant in active_tenants:
    
            settlements.append(TenantSettlement(
                tenant=tenant.name,
                apartment_settlement=apt_settlement.apartment,
                month=apt_settlement.month,
                year=apt_settlement.year,
                rent_pln=0.0,       
                bills_pln=share_of_bills,
                total_due_pln=-share_of_bills,
                balance_pln=0.0 ))
            
        return settlements