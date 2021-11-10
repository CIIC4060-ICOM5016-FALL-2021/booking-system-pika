class BasePerson:

  def deletePerson(self,p_id):
       cursor = self.conn.cursor()
       query = 'delete from "Person" where p_id = %s;'
       cursor.execute(query, (p_id,))
       deleted_rows = cursor.rowcount
       self.conn.commit()
       return deleted_rows !=0