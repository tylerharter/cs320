# Creating Your Virtual Machine

The lectures, instructions, and projects for this course are designed
for the Linux operating system (*Ubuntu 18.04 LTS Linux*, to be
precise -- there are many flavors/versions!).

Rather than replace Windows or Mac OS X on your computer, it will be
easier to rent a virtual machine (VM) in the cloud, which you will
then connect to remotely.  Knowing how to create virtual machines is
an important data-science skill because it makes your analysis more
*reproducible* -- if your code works in your virtual machine, and
other people know how to reconstruct a similar virtual machine for
themselves (with the same operating system and programs installed),
they're more likely to be able to reproduce the same results by
running your code.

At the low-end, renting a VM costs about
$10-20/month.  Fortunately, the major cloud providers often provide
free credit for students and new users, so you'll likely pay little or
(hopefully) nothing this semester.

We provide directions for two major cloud providers: GCP (Google's
cloud) and Azure (Microsoft's cloud).  If you want to find another
way/place to use Ubuntu 18.04 LTS and install Jupyter, that's fine
too, and you can skip this lab (though we will only support the first
two options during office hours).

Choose one of the following for the remainder of this lab:

1. [GCP Directions](gcp/README.md).  At the time these directions were written, Google offers $300 of credit for new users.  Unfortunately, the credits must be used within 90 days, which doesn't quite cover a semester.  Fortunately, Google gave me educational credits ($50/student) to use for CS 320, which should cover you.  I'll be sending details in a Canvas announcement about how to redeem these.
2. [Azure Directions](azure/README.md).  At the time these directions were written, Microsoft offers students $100/year of credit per year.

Note that this is our first semester giving Azure as a second option,
so most examples/documentation will be based on the first option
above.

You'll use the VM you create for the rest of the semester, so take
notes on how to use SSH and connect to Jupyter.
