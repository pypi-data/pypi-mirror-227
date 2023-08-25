# coding: utf-8
from pyotrs.lib import DynamicField

from .update_ticket_DF import UpdateTicketDF


class MoveSharingDataMobileTickets(UpdateTicketDF):
    """
    Set DF compartidesEnProvisio to OTRS mobile tickets.
    """

    def _prepare_dynamic_fields(self):
        return [DynamicField(name="compartidesEnProvisio", value=1)]
