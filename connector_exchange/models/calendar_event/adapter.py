# -*- coding: utf-8 -*-
# Author: Damien Crier
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from pyews.ews.data import FolderClass
from ...unit.backend_adapter import ExchangeAdapter
from ...backend import exchange_2010


@exchange_2010
class EventBackendAdapter(ExchangeAdapter):
    _model_name = ['exchange.calendar.event']

    def create(self, folder, exchange_obj, user):
        invit = "SendToNone"
        if user.send_calendar_invitations:
            invit = "SendToAllAndSaveCopy"
        return self.ews.CreateCalendarItem(folder, exchange_obj,
                                           send_meeting_invitations=invit)

    def write(self, external_id, exchange_obj, user):
        invit = "SendToNone"
        if user.send_calendar_invitations:
            invit = "SendToChangedAndSaveCopy"
        return self.ews.UpdateCalendarItems([exchange_obj],
                                            send_meeting_invitations=invit)

    def find_folder(self, odoo_folder):
        self.ews.get_root_folder()
        exchange_folder = self.ews.root_folder.FindFolderByDisplayName(
            str(odoo_folder.name),
            types=[FolderClass.Calendars],
            recursive=True)
        return exchange_folder[0]

    def create_folder(self, odoo_folder):
        self.ews.get_root_folder()

        self.ews.CreateFolder(
            self.ews.root_folder.Id,
            [(str(odoo_folder.name), FolderClass.Calendars)]
            )

        # The folder returned by ews.CreateFolder contains only an Id.
        # Read the rest of the data
        exchange_folder = self.ews.root_folder.FindFolderByDisplayName(
            str(odoo_folder.name),
            types=[FolderClass.Calendars],
            recursive=True)

        return exchange_folder[0]
