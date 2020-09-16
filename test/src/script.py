

# cmd to run script
# ./manage.py shell < myscript.py




from polls.models import Ptype;
from polls.models import PollItem;
from polls.models import PollVote;
from polls.models import PollFav;
from users.models import PUser;
from django.contrib.auth.models import User





##### Changing the polltypes and pollitems to one user #####

# newuser = User.objects.filter()
# for i in newuser:
# 	print (i)
# 	print (i.id)

# tcuser = User.objects.get(id=21)
# print (tcuser)
# print ("change to")


# curruser = User.objects.get(id=7)
# print (curruser)
# print ("current")

# existing_pt = Ptype.objects.filter();
# for i in existing_pt:
# 	i.c_user = tcuser
# 	print (i)
# 	i.save()

# existing_pi = PollItem.objects.filter();
# for i in existing_pi:
# 	i.user_submit = tcuser
# 	print (i)
# 	i.save()

# existing_pv = PollVote.objects.filter(vote_user=curruser);
# for i in existing_pv:
# 	print(i)
# 	i.delete()

# existing_pf = PollFav.objects.filter(fav_user=curruser);
# for i in existing_pf:
# 	print(i)
# 	i.delete()


# existing_pu = PUser.objects.filter(user=curruser);
# for i in existing_pu:
# 	print(i)
# 	i.delete()






###### deactivate previous polls #####

# from polls.models import Ptype;
# from polls.models import PollItem;

# existing_pt = Ptype.objects.filter();
# for i in existing_pt:
# 	i.active = False
# 	print (i)
# 	i.save();

# existing_pi = PollItem.objects.filter();
# for i in existing_pi:
# 	i.allowed = False
# 	print (i)
# 	i.save();




#### change the slug #####

# from polls.models import Ptype;

# existing_polls = Ptype.objects.filter();
# for individual_poll in existing_polls:
# 	individual_poll.slug = '1'
# 	individual_poll.save();

# print ("script completed")
