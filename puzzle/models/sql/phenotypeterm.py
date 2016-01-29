# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .models import BASE


class PhenotypeTerm(BASE):

    """Represent a HPO phenotype term."""

    __tablename__ = "phenotype_term"

    id = Column(Integer, primary_key=True)
    phenotype_id = Column(String(32), nullable=False)
    description = Column(String(128))

    case_id = Column(Integer, ForeignKey('case.id'))
    case = relationship('Case', backref=('phenotype_terms'))

    @property
    def hpo_link(self):
        """Return a HPO link."""
        return ("http://compbio.charite.de/hpoweb/showterm?id={}"
                .format(self.phenotype_id))

    @property
    def omim_link(self):
        """Return a OMIM phenotype link."""
        return "http://www.omim.org/entry/{}".format(self.phenotype_id)

    def __repr__(self):
        return ("PhenotypeTerm(phenotype_id={this.phenotype_id})"
                .format(this=self))
