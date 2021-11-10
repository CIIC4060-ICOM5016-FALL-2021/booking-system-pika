class BasePerson:



  def UpdatePerson(self,p_id,p_fname, p_lname, p_role, p_email, p_phone, p_gender):
   cursor = self.conn.cursor()
   query = 'update "Person" ' \
               'set p_fname = %s, p_lname= %s, p_role = %s, p_email= %s , p_phone = %s ,p_gender= %s ' \
               'where p_id = %s '
   cursor.execute(query, (p_fname, p_lname, p_role, p_email, p_phone, p_gender, p_id))
   self.conn.commit()
   return True

  def deletePerson(self,p_id):
       cursor = self.conn.cursor()
       query = 'delete from "Person" where p_id = %s;'
       cursor.execute(query, (p_id,))
       deleted_rows = cursor.rowcount
       self.conn.commit()
       return deleted_rows !=0