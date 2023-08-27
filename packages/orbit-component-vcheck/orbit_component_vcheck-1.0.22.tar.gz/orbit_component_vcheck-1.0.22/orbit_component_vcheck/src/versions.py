from orbit_component_vcheck.schema.Versions import VersionsCollection, VersionsTable
from rich.console import Console
from rich.table import Table
from datetime import datetime


class Versions:

    COLLECTIONS = [VersionsCollection]

    def __init__ (self, odb):
        self._odb = odb

    def setup (self):
        for cls in self.COLLECTIONS:
            cls().open(self._odb)
        return self

    def list (self):
        table = Table(
            title='Registered Versions',
            title_style='bold green',
        )
        rstyle = 'cyan'
        hstyle = 'deep_sky_blue4'
        table.add_column('Product Name',    style=rstyle, header_style=hstyle, no_wrap=True)
        table.add_column('Version String',  style=rstyle, header_style=hstyle, no_wrap=True)
        table.add_column('Last Updated',    style=rstyle, header_style=hstyle, no_wrap=True)

        for result in VersionsCollection():
            doc = result.doc
            table.add_row(
                str(doc._product),
                str(doc._version),
                str(doc.last_seen))
        Console().print(table)
        print()

    def add (self, product, version):
        doc = VersionsTable().from_product(product)
        doc.update({'version': version, 'when': datetime.now().timestamp()})
        if doc.isValid:
            old_version = doc._version
            doc.save()
            print(f'product ({product}) updated from {old_version} to {version}')
        else:
            doc.update({'product': product})
            doc.append()
            print(f'product ({product}) version ({version}) appended')

    def delete (self, product):
        doc = VersionsTable().from_product(product)
        if not doc.isValid:
            print(f'product ({product}) was not found')
        else:
            doc.delete()
            print(f'product ({product}) deleted')
    