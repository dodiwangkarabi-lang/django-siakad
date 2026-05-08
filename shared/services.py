from django.db import transaction

class BaseModelService:
    model = None
        
    def _get_all_update_fields(self, exclude:list=[]):
        
        return [
            field.name
            for field in self.model._meta.fields
            if field.name not in exclude
        ]
        
    # @transaction.atomic
    def bulk_save(self, data_list, unique_fields:list, exclude:list=["id", "nim", "created_at"]):
        with transaction.atomic():
            
            # convert string → field object
            unique_field_objs = [
                self.model._meta.get_field(f) if isinstance(f, str) else f
                for f in unique_fields
            ]
        
            objs = [
                self.model(**data)
                for data in data_list
            ]
            
            self.model.objects.bulk_create(
                objs,
                update_conflicts=True,
                unique_fields=unique_fields,
                update_fields=self._get_all_update_fields(exclude),
                batch_size=1000
            )
            
            # return self.model.objects(objs)
           
            # return self.model.objects.bulk_create(
            #     objs,
            #     update_conflicts=True,
            #     unique_fields=unique_fields, # penentu bentrok
            #     # unique_fields=unique_field_objs, # penentu bentrok
            #     # update_fields=["status", "prodi"], # field yang diupdate
            #     update_fields=self._get_all_update_fields(exclude),
            #     batch_size=1000
            # )
            
        return 