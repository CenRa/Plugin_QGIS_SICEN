# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SICEN
                                 A QGIS plugin
 Filtre sur données SICEN
                             -------------------
        begin                : 2014-10-17
        copyright            : (C) 2014 by Guillaume COSTES
        email                : guillaume.costes@espaces-naturels.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load SICEN class from file SICEN
    from sicen import SICEN
    return SICEN(iface)
