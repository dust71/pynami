# -*- coding: utf-8 -*-
"""
Schemas for operations on members
"""
import json
from marshmallow import fields, pre_load, post_dump

from .base import BaseSchema, BaseSearchSchema, BaseModel, BaseSearchModel


class NamiKonto(BaseModel):
    """
    Holds information about bank account and payment method of the member.

    This class is intended to be instantiated by calling the
    :meth:`~marshmallow.Schema.load` method on a corresponding data dictionary.
    """
    def __repr__(self):
        return f'<Kontodaten(Id: {self.id})>'

    def __str__(self):
        return f'{self.zahlungsKondition}'


class NamiKontoSchema(BaseSchema):
    """
    Schema class for bank account and payment method information.

    This Schema will is :std:doc:`nested <nesting>` inside a
    :class:`MitgliedSchema` and there should be no other use for it.
    """
    __model__ = NamiKonto

    id = fields.String()
    """int: |NAMI| internal id of this payment details"""
    zahlungsKonditionId = fields.Integer()
    """int: Id corresponding to the kind of payment"""
    mitgliedsNummer = fields.Integer()
    """int: |DPSG| member id"""
    institut = fields.String()
    """str: Bank"""
    kontoinhaber = fields.String()
    """str: Account holder"""
    kontonummer = fields.String()
    """str: Account number"""
    bankleitzahl = fields.String()
    """str: Bank sort code"""
    iban = fields.String()
    """str: |IBAN|"""
    bic = fields.String()
    """str: |BIC|"""
    zahlungsKondition = fields.String(load_only=True)
    """str: Kind of payment (e.g. ``'Std Lastschrift'``). This attribute is not
    dumped when updating a `Mitglied`."""

    @pre_load
    def id_to_str(self, data, **kwargs):
        """
        For some reason the |NAMI| gives the id of the payment details as an
        :obj:`integer <int>`, but when you want to update a member it has be a
        :obj:`string <str>`. Therefore this method converts incoming ids to a
        :obj:`str` object before loading them by making use of the
        :func:`~marshmallow.decorators.pre_load` decorator.

        Args:
            data (dict): Data dictionary to be loaded

        Returns:
            dict: Corrected data dictionary
        """
        data['id'] = f'{data["id"]}'
        return data

    @post_dump
    def double_dump(self, data, **kwargs):
        """
        Incoming data sets are nicely formatted :mod:`json` strings which can
        be loaded easily into the Schema but when you update a Mitglied all
        payment details have to formatted into a :mod:`json` string and all
        attributes have to be in a certain order.
        To achieve this the :func:`~marshmallow.decorators.post_dump` decorator
        is used.

        Args:
            data (dict): Already dumped data set

        Returns:
            str: A :mod:`json` formatted string
        """
        return json.dumps(data, separators=(',', ':'))


class SearchMitglied(BaseSearchModel):
    """
    Main class for a Mitglied which came up as a search result. Unfortunately
    there cannot be just one Mitglied class because the search results lack
    crucal imformation (e.g. payment details).
    """
    _tabkeys = ['mitgliedsNummer', 'vorname', 'nachname', 'geburtsDatum']
    _field_blacklist = ['representedClass', 'mglType', 'staatsangehoerigkeit',
                        'status', 'geschlecht', 'eintrittsdatum', 'id',
                        'wiederverwendenFlag',  'descriptor', 'version',
                        'lastUpdated', 'id_id']

    def __repr__(self):
        return f'<SearchMitglied({self.descriptor})>'

    def __str__(self):
        return f'{self.descriptor}'

    def get_mitglied(self, nami):
        """
        Create a real :class:`Mitglied` form the search result by getting the
        corresponding data set through the member id.

        Args:
            nami (:class:`~pynami.nami.NaMi`): Main |NAMI| class

        Returns:
            Mitglied: The Mitglied object corresponding to this search result.
        """
        return nami.mitglied(self.id, 'GET')


class SearchMitgliedSchema(BaseSearchSchema):
    """
    Schema class for :class:`SearchMitglied`.

    For some reason attribute naming in the |NAMI| is a bit inconsistent
    between a Mitglied which comes up as a search result and one that is
    addressed directly by its id.
    """
    __model__ = SearchMitglied

    entries_austrittsDatum = fields.DateTime(attribute='austrittsDatum',
                                             allow_none=True)
    """:class:`~datetime.datetime`: Date of the end of membership"""
    entries_beitragsarten = fields.String(attribute='beitragsarten')
    """str: Fee type"""
    entries_eintrittsdatum = fields.DateTime(attribute='eintrittsdatum')
    """:class:`~datetime.datetime`: Start of membership"""
    entries_email = fields.String(attribute="email")
    """str: Primary member email"""
    entries_emailVertretungsberechtigter = \
        fields.String(attribute="emailVertretungsberechtigter",
                      allow_none=True)
    """str: Email address of an authorized representative."""
    entries_ersteTaetigkeitId = \
        fields.Integer(attribute='ersteTaetigkeitId', allow_none=True)
    """int: Id of the first activity. Defaults to ``null``."""
    entries_ersteUntergliederungId = \
        fields.Integer(attribute='ersteUntergliederungId', allow_none=True)
    """int: Id of the first tier. This may be empty."""
    entries_fixBeitrag = fields.String(attribute="fixBeitrag", allow_none=True)
    """str: Defaults to ``null``."""
    entries_geburtsDatum = fields.DateTime(attribute='geburtsDatum')
    """:class:`~datetime.datetime`: Birth date"""
    entries_genericField1 = fields.String(attribute="genericField1",
                                          allow_none=True)
    """str: Not sure why these even exist."""
    entries_genericField2 = fields.String(attribute="genericField2",
                                          allow_none=True)
    """str: Not sure why these even exist."""
    entries_geschlecht = fields.String(attribute='geschlecht')
    """str: Gender"""
    entries_id = fields.Integer(attribute='id_id')
    """int: |NAMI| internal id (not |DPSG| member nummer)."""
    entries_jungpfadfinder = fields.String(attribute='jungpfadfinder')
    """str: Tier field. Not sure what it is for."""
    entries_konfession = fields.String(attribute='konfession')
    """str: Confession"""
    entries_kontoverbindung = fields.String(attribute='kontoverbindung')
    """str: Account details. For some reason this is not always transmitted and
    may therefore be empty."""
    entries_lastUpdated = fields.DateTime(attribute='lastUpdated')
    """:class:`~datetime.datetime`: Date of the last update"""
    entries_mglType = fields.String(attribute='mglType')
    """str: Type of membership (e.g. ``'Mitglied'``)"""
    entries_mitgliedsNummer = fields.Integer(attribute='mitgliedsNummer')
    """int: |DPSG| member number"""
    entries_nachname = fields.String(attribute='nachname')
    """str: Surname"""
    entries_pfadfinder = fields.String(attribute='pfadfinder')
    """str: Tier field. Not sure what it is for."""
    entries_rover = fields.String(attribute='rover')
    """str: Tier field. Not sure what it is for."""
    entries_rowCssClass = fields.String(attribute='rowCssClass')
    """str: Unused. The purpose could not be dount out."""
    entries_spitzname = fields.String(attribute='spitzname')
    """str: Nickname"""
    entries_staatangehoerigkeitText = \
        fields.String(attribute='staatangehoerigkeitText')
    """str: Extra nationality info. Empty in most cases."""
    entries_staatsangehoerigkeit = \
        fields.String(attribute='staatsangehoerigkeit')
    """str: Nationality"""
    entries_status = fields.String(attribute='status')
    """str: If the member is active or not"""
    entries_stufe = fields.String(attribute='stufe')
    """str: Current tier"""
    entries_telefax = fields.String(attribute='telefax')
    """str: Fax number. Who uses these anyway today?"""
    entries_telefon1 = fields.String(attribute='telefon1')
    """str: First phone number"""
    entries_telefon2 = fields.String(attribute='telefon2')
    """str: Second  phone number"""
    entries_telefon3 = fields.String(attribute='telefon3')
    """str: Third phone number"""
    entries_version = fields.Integer(attribute='version')
    """int: History version number"""
    entries_vorname = fields.String(attribute='vorname')
    """str: First name"""
    entries_wiederverwendenFlag = \
        fields.Boolean(attribute='wiederverwendenFlag')
    """bool: If the member data may be used after the membership ends"""
    entries_woelfling = fields.String(attribute='woelfling')
    """str: Tier field. Not sure what it is for."""
    entries_gruppierung = fields.String(allow_none=True,
                                        attribute='gruppierung')
    """str: Group name including its id"""
    entries_gruppierungId = fields.String(allow_none=True,
                                          attribute='gruppierungId')
    """str: Group id as a string"""


class Mitglied:
    """
    Main class representing a |NAMI| Mitglied

    This class overwrites the :meth:`~object.__getattr__` and
    :meth:`~object.__setattr__` methods so that attributes of this class can be
    handled in a convinient way. It is intended to be instantiated by calling
    the :meth:`~marshmallow.Schema.load` method on a corresponding data
    dictionary.
    """
    _tabitems = ['mitgliedsNummer', 'vorname', 'nachname', 'geburtsDatum',
                 'strasse', 'stufe']
    _field_blacklist = ['genericField1']

    def __init__(self, **kwargs):
        self.data = kwargs

    def __repr__(self):
        return f'<Mitglied({self.nachname}, {self.vorname})>'

    def __str__(self):
        return f'{self.vorname} {self.nachname}'

    def __getattr__(self, name):
        try:
            return super().__getattr__(name)
        except AttributeError:
            return self.data[name]

    def __setattr__(self, name, value):
        try:
            super().__setattr__(name, value)
        except AttributeError:
            self.data[name] = value
            
    def __getstate__(self):
        return vars(self)

    def __setstate__(self, state):
        vars(self).update(state)

    def update(self, nami):
        """
        Writes the possibly changed values to the |NAMI|

        Args:
            nami (:class:`~pynami.nami.NaMi`): Main class for communication
                with the |NAMI|

        Returns:
            Mitglied: The new Mitglied as it is returned by the |NAMI|
        """
        userjson = MitgliedSchema().dump(self.data)
        return nami.mitglied(self.id, 'PUT', json=userjson)


class MitgliedSchema(BaseSchema):
    """
    Schema class for a :class:`Mitglied`
    """
    __model__ = Mitglied

    austrittsDatum = fields.DateTime(allow_none=True, load_only=True)
    """:class:`~datetime.datetime`: Date of the end of membership"""
    beitragsart = fields.String(allow_none=True)
    """str: Fee type"""
    beitragsartId = fields.Integer(allow_none=True)
    """int: Id of the fee type"""
    eintrittsdatum = fields.DateTime()
    """:class:`~datetime.datetime`: Start of membership"""
    email = fields.String()
    """str: Primary member email"""
    emailVertretungsberechtigter = fields.String()
    """str: Email address of an authorized representative."""
    ersteTaetigkeit = fields.String(allow_none=True)
    """str: First activity. May be empty."""
    ersteTaetigkeitId = fields.Integer(allow_none=True, load_only=True)
    """int: Id of the first activity. Defaults to ``null``."""
    ersteUntergliederung = fields.String(allow_none=True)
    """str: First tier. May be empty"""
    ersteUntergliederungId = fields.Integer(allow_none=True, load_only=True)
    """int: Id of the first tier. This may be empty."""
    fixBeitrag = fields.String(allow_none=True)
    """str: Defaults to ``null``."""
    geburtsDatum = fields.DateTime()
    """:class:`~datetime.datetime`: Birth date"""
    genericField1 = fields.String(allow_none=True)
    """str: Not sure why these even exist."""
    genericField2 = fields.String(allow_none=True)
    """str: Not sure why these even exist."""
    geschlecht = fields.String()
    """str: Gender"""
    geschlechtId = fields.Integer(allow_none=True)
    """int: Gender id"""
    gruppierung = fields.String()
    """str: Group name including its id"""
    gruppierungId = fields.Integer(allow_none=True)
    """int: Group id

    .. note::

        In the search result (see :class:`SearchMitgliedSchema`) this comes as
        a :obj:`str`.

    """
    id = fields.Integer()
    """int: |NAMI| internal id (not |DPSG| member nummer)."""
    jungpfadfinder = fields.String(allow_none=True)
    """str: Tier field. Not sure what it is for."""
    konfession = fields.String(allow_none=True)
    """str: Confession"""
    konfessionId = fields.Integer(allow_none=True)
    """int: Id of the confession"""
    kontoverbindung = fields.Nested(NamiKontoSchema)
    """:class:`NamiKontoSchema`: Account details. In a search result this comes
    as a :obj:`str`."""
    land = fields.String()
    """str: Address country"""
    landId = fields.Integer()
    """int: Id of the address country"""
    lastUpdated = fields.DateTime(load_only=True)
    """:class:`~datetime.datetime`: Date of the last update. This value is not
    dumped when updating a :class:`Mitglied`."""
    mglType = fields.String()
    """str: Type of membership (e.g. ``'Mitglied'``)"""
    mglTypeId = fields.String(load_only=True)
    """str: Id of the type of membership (typically just the value in
    uppercase)."""
    mitgliedsNummer = fields.Integer(load_only=True)
    """int: |DPSG| member number"""
    nachname = fields.String()
    """str: Surname"""
    nameZusatz = fields.String(allow_none=True)
    """str: Extra name info"""
    ort = fields.String(allow_none=True)
    """str: Address city"""
    pfadfinder = fields.String(allow_none=True)
    """str: Tier field. Not sure what it is for."""
    plz = fields.String(allow_none=True)
    """str: Postal code"""
    region = fields.String(allow_none=True)
    """str: A `Bundesland` or foreign country"""
    regionId = fields.Integer(allow_none=True)
    """int: Region id"""
    rover = fields.String(allow_none=True)
    """str: Tier field. Not sure what it is for."""
    sonst01 = fields.Boolean(allow_none=True)
    """bool: Another generic field. Defaults to :data:`False`."""
    sonst02 = fields.Boolean(allow_none=True)
    """bool: Another generic field. Defaults to :data:`False`."""
    spitzname = fields.String(allow_none=True)
    """str: Nickname"""
    staatsangehoerigkeit = fields.String(allow_none=True)
    """str: Nationality"""
    staatsangehoerigkeitId = fields.Integer(allow_none=True)
    """int: Id of the nationality"""
    staatsangehoerigkeitText = fields.String(allow_none=True)
    """str: Extra nationality info. Empty in most cases."""
    status = fields.String(allow_none=True)
    """str: If the member is active or not"""
    strasse = fields.String(allow_none=True)
    """str: Address information"""
    stufe = fields.String(allow_none=True)
    """str: Current tier"""
    telefax = fields.String(allow_none=True)
    """str: Fax number. Who uses these anyway today?"""
    telefon1 = fields.String(allow_none=True)
    """str: First phone number"""
    telefon2 = fields.String(allow_none=True)
    """str: Second  phone number"""
    telefon3 = fields.String(allow_none=True)
    """str: Third phone number"""
    version = fields.Integer()
    """int: History version number"""
    vorname = fields.String(allow_none=True)
    """str: First name"""
    wiederverwendenFlag = fields.Boolean()
    """bool: If the member data may be used after the membership ends"""
    woelfling = fields.String(allow_none=True)
    """str: Tier field. Not sure what it is for."""
    zeitschriftenversand = fields.Boolean(allow_none=True)
    """bool: If the member gets the |DPSG| newspaper."""

    class Meta(BaseSchema.Meta):
        """
        Extended :class:`marshmallow.Schema.Meta` class for further
        configuration
        """
        ordered = True
        """bool: This is nesseccary for the payment deatils to be dumped in the
        corrent order."""

