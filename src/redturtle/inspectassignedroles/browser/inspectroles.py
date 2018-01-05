"""
This module export all sharing configuration from a plone site
"""

import string
import tempfile
from copy import deepcopy

import xlsxwriter
from Products.Five.browser import BrowserView
from plone import api
try:
    from collections import OrderedDict
except:
    from ordereddict import OrderedDict
from Products.CMFPlone.utils import safe_unicode
from redturtle.inspectassignedroles.utils import EphemeralStreamIterator


class InspectRoles(BrowserView):
    """
    This view check for all assigned roles in portal
    """

    USERS_OR_GROUP = {}

    def get_user_or_group(self, entry):
        """
        Get the user or group fullname/title
        """
        if entry not in self.USERS_OR_GROUP:
            member = api.user.get(entry)
            if member:
                if member.getProperty('fullname'):
                    self.USERS_OR_GROUP[entry] = member.getProperty('fullname')
                    return self.USERS_OR_GROUP[entry]
            group = api.group.get(groupname=entry)
            if group:
                if group.getProperty('title'):
                    self.USERS_OR_GROUP[entry] = group.getProperty('title')
                    return self.USERS_OR_GROUP[entry]

        return self.USERS_OR_GROUP[entry]

    def get_assigned_local_roles(self, brains, roles):
        """
        Get the assigned local roles in portal
        """
        entry = OrderedDict()
        entry['title'] = ''
        entry['url'] = ''
        for role in roles:
            entry[role] = []

        assigned_local_roles = []
        for brain in brains:
            content = brain.getObject()
            currlr = content.__ac_local_roles__
            # check if we have only Owner
            if not currlr:
                continue
            if currlr == {'admin': ['Owner']} or\
               (len(currlr.keys()) == 1 and currlr.values() == [['Owner']]):
                continue

            # avoid to edit original
            newentry = deepcopy(entry)
            newentry['url'] = brain.getURL()
            newentry['title'] = brain.Title

            for user in currlr:
                for role in roles:
                    if role in currlr[user]:
                        newentry[role].append(self.get_user_or_group(user))
                assigned_local_roles.append(newentry)

        return assigned_local_roles

    def get_site_roles(self, roles):
        """
        Get the assigned global roles
        """
        global_roles = []
        roles.insert(0, 'Authenticated')
        entry = OrderedDict()
        entry['userid'] = ''
        entry['fullname'] = ''
        for role in roles:
            entry[role] = ''

        for member in api.user.get_users():
            newentry = deepcopy(entry)
            newentry['userid'] = member.id
            newentry['fullname'] = self.get_user_or_group(member.id)
            for role in roles:
                if role in member.getRoles():
                    newentry[role] = 'x'
            global_roles.append(newentry)
        return global_roles

    def write_global_roles(self, workbook, site_roles, header_format,
                           cell_format, roles):
        """
        Write discovered global roles to excel file
        """
        translate = self.context.translate
        worksheet = workbook.add_worksheet('RuoliGlobali')
        header = ['Login', 'Nome']
        header.extend(roles)
        letters = string.ascii_uppercase

        for i, label in enumerate(header):
            letter = letters[i]
            worksheet.write('{0}1'.format(letter),
                            safe_unicode(translate(label, domain='plone')),
                            header_format)
        counter = 2
        for row in site_roles:
            for i, key in enumerate(row.keys()):
                if i > 1:
                    worksheet.write('{0}{1}'.format(letters[i], counter),
                                    safe_unicode(row[key]), cell_format)
                else:
                    worksheet.write('{0}{1}'.format(letters[i], counter),
                                    safe_unicode(row[key]))
            counter += 1
        return

    def write_local_roles(self, workbook, local_roles, header_format, roles):
        """
        Write discovered local roles to excel file
        """
        translate = self.context.translate
        worksheet = workbook.add_worksheet('RuoliLocali')
        header = ['Url', 'Titolo']
        roles.remove('Authenticated')
        header.extend(roles)
        letters = string.ascii_uppercase

        for i, label in enumerate(header):
            letter = letters[i]
            worksheet.write('{0}1'.format(letter),
                            safe_unicode(translate(label, domain='plone')),
                            header_format)

        counter = 2
        for row in local_roles:
            for i, key in enumerate(row.keys()):
                if i > 1:
                    worksheet.write('{0}{1}'.format(letters[i], counter),
                                    ', '.join(row[key]).decode('utf-8'))
                else:
                    worksheet.write('{0}{1}'.format(letters[i], counter),
                                    row[key].decode('utf-8'))
            counter += 1
        return

    def write_xlsx(self, assigned_local_roles, site_roles, roles):
        """
        Write on excel
        """
        filename = 'ruoliassegnati.xlsx'
        filepath = '{0}/{1}'.format(tempfile.mkdtemp(), filename)
        workbook = xlsxwriter.Workbook(filepath)
        cell_format = workbook.add_format({
            'align': 'center'
        })
        header_format = workbook.add_format({
            'border': 1,
            'color': 'white',
            'bg_color': '#808080',
            'bold': True,
            'valign': 'vcenter',
        })

        self.write_global_roles(workbook, site_roles,
                                header_format, cell_format, roles)
        self.write_local_roles(workbook, assigned_local_roles,
                               header_format, roles)

        workbook.close()
        return filepath

    def __call__(self):
        """
        from all objects get local roles
        """
        brains = api.portal.get_tool(name='portal_catalog')()
        brains = sorted(brains, key=lambda brain: brain.getPath())
        roles = [r for r in
                 api.portal.get_tool(name='portal_membership').getPortalRoles()
                 if r != 'Owner']

        assigned_local_roles = self.get_assigned_local_roles(brains, roles)
        site_roles = self.get_site_roles(roles)

        filepath = self.write_xlsx(assigned_local_roles, site_roles, roles)
        response = self.request.RESPONSE
        streamed = EphemeralStreamIterator(filepath, delete_parent=False)
        mime =\
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response.setHeader('Content-type',
                           '{0};charset={1}'.format(mime, 'utf-8'))
        response.setHeader('Content-Length', str(len(streamed)))
        response.setHeader("Content-Disposition",
                           "attachment; filename=\"ruoliassegnati.xlsx\"")
        return streamed
