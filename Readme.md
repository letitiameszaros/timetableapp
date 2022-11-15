# Timetable reschedule application #

Problem: Given a file containing the timetable of a student (day, starting hour, ending hour and nameid of classes in every line) (timetable.txt)
and a file with all the possible timeslots during the week the student can attend the classes (with other groups for example) (options.txt)
(same structure as timetable file), make an application that gets an entry like the line of the files (day, starting hour, ending hour, nameid)
from keyboard input and if possible, reschedules/rearranges the timetable in such a way that the input entry can be inserted into the timetable at the desired time and day.
(Insert a new class or activity into the timetable.) The student only has to attend every class once a week and every class and entry (input as well) should only be 2 hours long, starting and ending
with even numbers, within the 8-20 time period.

How I solved it: I stored the timetable in a dictionary, using the days as keys, I also stored the alternative timeslots
list in a dictionary with tuples as values, but using the nameid of the courses as the keys this time. With the help ofthese structures 
I used a recursive algorithm to go through all possible course swap and alternative course options to see if it is possible to insert the given activity.
In case some routes are explored but they turn out to not be possible to be used for insertion, their effect is erased (backtracking).
If the insertion was successful, newtimetable.txt and newoptions.txt files are generated which can be reused as inputs to further edit the timetable.
The solution has its flaws. For example the correctness of the input is not always checked and there are some ways to optimize or tidyup the code
(storing the ending hour of courses has no point, since we never need it, but it got left in because initially i wanted to make
the program more complex, capable of working with any length event, not just 2 hours long ones, but being short of time I stack to the simpler version.)
