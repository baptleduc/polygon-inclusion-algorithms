class Cellule:
    def __init__(self,value = None):
        self.value = value
        self.prec = None
        self.suiv = None
        #print("prec = ",self.tab[value].prec.value)
        #print("suiv = ",self.tab[value].suiv.value)
        
    def __str__(self):
        if self.suiv:
            return str(self.value) + " -> " + str(self.suiv)
        return str(self.value)

    def is_alone(self):
        return (not self.prec) and (not self.suiv)

    def is_head(self):
        return not self.prec

    def is_queue(self):
        return not self.suiv
    
    def delete(self):
        if self.is_alone():
            self.value = None
            return
        if self.is_head():
            self.suiv.prec = None
            return
        if self.is_queue():
            self.prec.suiv = None
            return
        self.prec.suiv = self.suiv
        self.suiv.prec = self.prec

    def insert_head(self,value):
        self.prec = Cellule(value)
        self.prec.suiv = self

class ListeTab:
    """
    A linked list but with an array where the i-th element is the element of the list with the value i
    """
    
    def __init__(self,taille):
        """
        initialization of the linked list
        """
        self.tab = [None] * taille
        self.head = None

    def __str__(self):
        return str(self.head)
    
    def insert(self,value):
        """
        insert a value at the head of the linked list
        Args: 
           value : int the value of the Cellule to insert
        """
        if not self.head:
            self.head = Cellule(value)
        else:
            self.head.insert_head(value)
            self.head = self.head.prec
        self.tab[value] = self.head
    def delete(self,value):
        """
        delete the element of the list with the value value and return its childs
        Args:
            value : int the value of the Cellule to delete
        Return:
            A Cellule object which is the child of the element deleted
        """
        temp = self.tab[value].suiv
        if self.tab[value].is_alone():
            self.head = None
        elif self.tab[value].is_head():
            self.tab[value].delete()
            self.head = self.head.suiv
        else:
            self.tab[value].delete()
        tab_temp = []
        while temp:
            tab_temp.append(temp.value)
            temp = temp.suiv
        return tab_temp
            
            
