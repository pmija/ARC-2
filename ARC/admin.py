from django.contrib import admin
from .models import Ref_UserType
from .models import Ref_UserStatus
from .models import User
from .models import ActualResidency
from .models import Ref_Term
from .models import Ref_Laboratory
from .models import Ref_Schedule
from .models import ResidencyTimeSlot
from .models import StudentResidencySchedule
from .models import Ref_AuditAction
from .models import Inventory
from .models import AuditTable_Inventory
from .models import Group
from .models import Ref_Degree
from .models import Ref_Department


# Register your models here.
admin.site.register(Ref_UserType)
admin.site.register(Ref_UserStatus)
admin.site.register(User)
admin.site.register(ActualResidency)
admin.site.register(Ref_Term)
admin.site.register(Ref_Laboratory)
admin.site.register(Ref_Schedule)
admin.site.register(ResidencyTimeSlot)
admin.site.register(StudentResidencySchedule)
admin.site.register(Ref_AuditAction)
admin.site.register(Inventory)
admin.site.register(AuditTable_Inventory)
admin.site.register(Group)
admin.site.register(Ref_Degree)
admin.site.register(Ref_Department)
