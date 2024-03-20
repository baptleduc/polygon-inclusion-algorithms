class ListeChainee:
    def __init__(self,value = None):
        self.value = value
        self.prec = None
        self.suiv = None

    def __str__(self):
        if self.suiv:
            return str(self.value) + " -> " + str(self.suiv)
        return str(self.value)

    def delete(self, val):
        if self.value == val:
            if self.prec:
                if self.suiv:
                    cell = self.prec
                    self.suiv.prec = self.prec
                    self.prec.suiv = self.suiv
                    return cell
                cell = self.prec
                self.prec.suiv = None
                return cell
            if self.suiv:
                self.suiv.prec = None
                return self.suiv
            self.value = None
            return self
        assert(self.prec)
        return self.prec.delete(val)

    def insert(self,val):
        if self.value is not None:
            self.suiv = ListeChainee(val)
            self.suiv.prec = self
            return self.suiv
        self.value = val
        return self

    def affiche(self):
        if self.prec:
            self.prec.affiche()
            return
        print(str(self))

    def go_end(self):
        if self.suiv:
            return self.suiv.go_end()
        return self
