from DAO.database_access import database_access

class forn_prod_DAO:
    def __init__(self):
        self.database_access_dao = database_access()
    
    def create_forn_prod(self, id_fornecedor, id_produto):
        
        try:
            query = f'''
            INSERT
            INTO forn_prod (fk_id_produto, fk_id_fornecedor)
            VALUES ('{id_produto}', '{id_fornecedor}');
    '''
            
            self.database_access_dao.execute_query(query)
            return True
        except:
            return False