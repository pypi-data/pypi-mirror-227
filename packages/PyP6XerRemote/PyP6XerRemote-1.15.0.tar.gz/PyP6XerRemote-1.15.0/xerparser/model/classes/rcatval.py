# PyP6XER
# Copyright (C) 2020, 2021 Hassan Emam <hassan@constology.com>
#
# This file is part of PyP6XER.
#
# PyP6XER library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License v2.1 as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyP6XER is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyP6XER.  If not, see <https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html>.


class RCatVal:
    obj_list = []

    def __init__(self, params):
        self.rsrc_catg_id = params.get('rsrc_catg_id').strip() if params.get('rsrc_catg_id') else None
        self.rsrc_catg_type_id = params.get('rsrc_catg_type_id').strip() if params.get('rsrc_catg_type_id') else None
        self.rsrc_catg_short_name = params.get('rsrc_catg_short_name').strip() if params.get('rsrc_catg_short_name') else None
        self.rsrc_catg_name = params.get('rsrc_catg_name').strip() if params.get('rsrc_catg_name') else None
        self.parent_rsrc_catg_id = params.get('parent_rsrc_catg_id').strip() if params.get('parent_rsrc_catg_id') else None
        RCatVal.obj_list.append(self)

    def get_id(self):
        return self.rsrc_catg_id

    def get_tsv(self):
        tsv = ['%R', self.rsrc_catg_id, self.rsrc_catg_type_id, self.rsrc_catg_short_name,
               self.rsrc_catg_name, self.parent_rsrc_catg_id]
        return tsv

    @classmethod
    def find_by_id(cls, id):
        obj = list(filter(lambda x: x.rsrc_catg_id == id, cls.obj_list))
        if obj:
            return obj[0]
        return obj

    def __repr__(self):
        return self.rsrc_catg_name