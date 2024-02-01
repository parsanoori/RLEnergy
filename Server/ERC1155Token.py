class ERC1155EnergyToken:
    def __init__(self, token_id: int, standard: str, carbon_value: int, carbon_type: str, owner: int,
                 issuance_year: int):
        self.token_id = token_id
        self.standard = standard
        self.carbon_value = carbon_value
        self.carbon_type = carbon_type
        self.owner = owner
        self.issuance_year = issuance_year

    def __str__(self) -> str:
        return f"ERC1155 Energy Token: {self.token_id}, Standard: {self.standard}, Carbon Value: {self.carbon_value}, Carbon Type: {self.carbon_type}, Owner: {self.owner}, Issuance Year: {self.issuance_year}"
