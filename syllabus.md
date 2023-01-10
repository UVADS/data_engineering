## Syllabus: DS 5559 – Data Engineering

### Contact

**Professor**  
Efrain Olivares  
dpy8wq@virginia.edu

**Teaching Assistant**  
Liz Thompson  
et7gav@virginia.edu

When emailing the professor or TAs: Please remember to include "DS 5559" in your email subject line.

### Course Description

Learn the essential environments and tools for data engineering. Topics include Linux, software development and testing,
database design and construction, creation and deployment of containers, and data load/transform/extraction. This course
will be very applied.

## Schedule of Topics 

| Week 	|Topics	|
|:---:	|:---	|
| 1 | Linux Fundamentals	|
| 2 | Software Skills 1 |
| 3 | Software Skills 2 |
| 4	| Software Testing |
| 5 | Database Design |
| 6 | Database Build and Use |
| 7 | CI/CD (Continuous Integration / Continuous Deployment) |
| 8 | Automation and Introduction to Containers |
| 9 | LTE I	(Load, Transform, Extract) |
| 10 | LTE II |
| 11 | Describing and Versioning Data |
| 12 | Service Monitoring |
 
### Learning Outcomes

Upon completion of this course, you are expected to be able to:
- confidently use Linux for navigating, inspecting, running scripts
- apply best practices in software development: 
  - write clean code
  - {update, version, create tests} for a package
  - use design patterns
- design a database that meets a set of requirements
- write SQL scripts that build and populate a database
- use `CircleCI` for automation of code testing and build
- use `Airflow` to build and run workflows: ingest data (e.g., from S3 bucket), transform and export
- properly describe and version your data
- understand how to monitor a service running in production

### Required Textbooks

**NOTE**: Nearly all of these books are electronically available for free

- The Linux Command Line, 2nd Edition: A Complete Introduction. William E. Shotts Jr. ISBN-10: 1593279523     
Freely available [here](https://www.oreilly.com/library/view/the-linux-command/9781492071235/?ar)

- Linux Bible, 10th Edition. Christopher Negus. ISBN-10: 1119578884     
Freely available [here](https://onlinelibrary-wiley-com.proxy01.its.virginia.edu/doi/book/10.1002/9781119578956)

- Clean code : a handbook of agile software craftsmanship. Robert C Martin. ISBN-10: 9780132350884  
Freely available [here](https://learning.oreilly.com/library/view/clean-code-a/9780136083238/?ar=)

- Beginning Database Design Solutions. Rod Stephens. ISBN-10: 0470385499  
Freely available [here](https://learning.oreilly.com/library/view/beginning-database-design/9780470385494/)

- Head First Design Patterns: A Brain-Friendly Guide, 1st Ed. E. Freeman, B. Bates, K. Sierra, Elisabeth Robson. ISBN-10: 9780596007126  
Freely available [here](https://learning.oreilly.com/library/view/head-first-design/0596007124/?ar=)

- Learning Python Design Patterns, 2nd Ed. Chetan Giridhar. ISBN-10: 178588803X  
Freely available [here](https://www.oreilly.com/library/view/learning-python-design/9781785888038/?ar)

- Test-Driven Machine Learning. Justin Bozonier. ISBN-10: 1784399086  
Freely available [here](https://www.oreilly.com/library/view/test-driven-machine-learning/9781784399085/?ar)

- Why programs fail: a guide to systematic debugging. Andreas Zeller. ISBN-10: 1558608664  
Freely available [here](https://www.oreilly.com/library/view/why-programs-fail/9780123745156/?ar)

- Test Driven Development: By Example. Kent Beck. ISBN-10: 9780321146533  
Freely available [here](https://www.oreilly.com/library/view/test-driven-development/0321146530/?ar)

- Python testing with pytest : simple, rapid, effective, and scalable. Brian Okken. ISBN-10: 1680508601  
Freely available [here](https://www.oreilly.com/library/view/python-testing-with/9781680502848/?ar)

- The Cucumber for Java Book: Behaviour-driven Development for Testers and Developers. S. Rose, M. Wynne, A. Hellesøy. ISBN-10: 1941222293  
Freely available [here](https://www.oreilly.com/library/view/the-cucumber-for/9781680500677/?ar)

- Docker: Up & Running, 2nd Edition. K. Matthias, S. P. Kane. ISBN: 9781492036739  
Freely available [here](https://learning.oreilly.com/library/view/docker-up/9781492036722/)

- Data pipelines with Apache Airflow. J. de Ruiter, B. Harenslak. ISBN: 9781617296901  
Freely available [here](https://learning.oreilly.com/videos/data-pipelines-with/9781617296901AU/)

- Snowflake Cookbook. H. Qureshi, H. Sharif. ISBN: 9781800560611  
Freely available [here](https://learning.oreilly.com/library/view/snowflake-cookbook/9781800560611/?ar=)

### Optional Textbooks

- Practical Vim: Edit Text at the Speed of Thought 2nd Edition. Drew Neil.    
Freely available [here](https://learning.oreilly.com/library/view/practical-vim-2nd/9781680501629/?ar=)

- bash Cookbook: Solutions and Examples for bash Users. Carl Albing.  
Freely available [here](https://learning.oreilly.com/library/view/bash-cookbook/0596526784/?ar=)

- Effective Python: 90 Specific Ways to Write Better Python (Effective Software Dev Series), 2nd Ed. Brett Slatkin. ISBN-10: 0134853989  
Freely available [here](https://learning.oreilly.com/library/view/effective-python-59/9780134034416/?ar=)

- Modern Python Standard Library Cookbook: Over 100 recipes to fully leverage the features of the standard library in Python. A. Molina. ISBN-10: 1788830822  
Freely available [here](https://learning.oreilly.com/library/view/modern-python-standard/9781788830829/?ar=)

### Compute Environments

There are two options:
- Use your own machine
- Use the **CEDS** virtual environment   
  [Access CEDS](https://rdweb.wvd.microsoft.com/arm/webclient/index.html)  
  [Instructions for using CEDS](https://github.com/UVADS/ds2001/blob/main/access_CEDS.docx)

### Delivery Mode Expectations

- Weekly 1-hr Live Sessions
    - Students complete assigned reading before live sessions
    - Live Sessions will consist of:
        - instructor giving code demos
        - students work on small coding assignments, with assistance from instructor/TA/potentially their peers
        - the instructor reviews coding solutions with the class
- Students submit assignments through Learning Management System (e.g., Collab)
- Expect to spend 10hrs/week on this course
- Office hours are held by instructor and TA (each are 1hr/week)

### Assessment

A weighted-average grade will be calculated as follows:  

|Component 	| Weight	|
|---	|:---:|
|Quizzes	|30%|
|Lab Assignments	|50%|
|Journaling	|15%|
|Attendance	|5%|

### Grading Scale                                                  

|Range 	| Grade	|
|---	|:---:|
|[98,100]	| A+|
|[93,98)	| A|
|[90,93)	| A-|
|[87,90)	| B+|
|[83,87)	| B|
|[80,83)	| B-|
|[77,80)	| C+|
|[73,77)	| C|
|[70,73)	| C-|
|<70	| F|
 

### Class Management
Email / Communication    
- Email is the best way to get in touch with the instructor

**Office Hours**
- Office hours will be held through Zoom. 
- If you cannot make it to office hours, the instructor can arrange a mutually agreeable appointment time. 

**Lab Assignments**
- There will be several lab assignments given throughout the semester. Specific grading criteria will be provided with each assignment.
- You are encouraged to first try to complete the lab by yourself.  If you work with others, be sure you understand all of the work, and that your final submission is your own work.
- Unless stated otherwise, please type your lab assignments and submit through Collab in the requested format
- When submitting lab assignments, don’t forget to write the assignment title, your name, your UVa computing ID, and date at the top of each assignment.
- In submission file, please include your initials in the filename.
- **IMPORTANT: Make sure you are submitting the correct file. Incorrect files are subject to the lateness policy below.**
- No lab assignments will be dropped.

**Lab Assignment Lateness Policy**
- Please submit assignments on time  
- If an issue will prompt late submission, email the TA in advance to explain the situation    
- If the lab is submitted late and it is not an excused lateness, 10% of the assignment total points will be deducted per day it is late   
- After 5 days of unexcused lateness, it will not be accepted

**Quizzes**
- There will be several quizzes throughout the semester that will assess your knowledge of the various topics
- Quizzes are based on readings and course content
- All quizzes are mandatory for all students to take
- **The quizzes should be done “closed book:”** please refrain from consulting any resources including notes, books, the web, devices, or other external media 
- If you know in advance that you will miss any of the scheduled quizzes, you must make arrangements in advance with the instructor. (At least one week in advance if possible, or as soon as you are able if an unforeseen event occurs preventing you from taking the quiz.)

### Spirit of the Course  
Students must attend live sessions. For the lab assignments and quizzes, you must submit your own work.

### Electronic Submission of Assignments  
All assignments must be submitted electronically through Collab by the specified due dates and times. It is crucial to complete all assigned work—failure to do so will likely result in failing the class.

### Technical Support Contacts  
UVaCollab: collab-support@virginia.edu

### Academic Integrity  

The School of Data Science relies upon and cherishes its community of trust. We firmly endorse, uphold, and embrace the University's Honor principle that students will not lie, cheat, or steal, nor shall they tolerate those who do. We recognize that even one honor infraction can destroy an exemplary reputation that has taken years to build. Acting in a manner consistent with the principles of honor will benefit every member of the community both while enrolled in the School of Data Science and in the future.

Students are expected to be familiar with the university honor code, including the section on academic fraud (https://honor.virginia.edu/). Each assignment will describe allowed collaborations, and deviations from these will be considered Honor violations. If you have questions on what is allowable, ask! Unless otherwise noted, exams and individual assignments will be considered pledged that you have neither given nor received help. (Among other things, this means that you are not allowed to describe problems on an exam to a student who has not taken it yet. You are not allowed to show exam papers to another student or view another student's exam papers while working on an exam.) Sending, receiving or otherwise copying electronic files that are part of course assignments are not allowed collaborations (except for those explicitly allowed in assignment instructions).
 
Assignments or exams where honor infractions or prohibited collaborations occur will receive a zero grade for that entire assignment or exam. Such infractions will also be submitted to the Honor Committee if that is appropriate. Students who have had prohibited collaborations may not be allowed to work with partners on remaining homework assignments.

### SDAC and Other Special Circumstances

If you have been identified as a Student Disability Access Center (SDAC) student, please let the Center know you are taking this class. If you suspect you should be an SDAC student, please schedule an appointment with them for an evaluation. I happily and discretely provide the recommended accommodations for those students identified by the SDAC. Please contact your instructor one week before an exam so we can make appropriate accommodations.
Website:  https://www.studenthealth.virginia.edu/sdac
If you are affected by a situation that falls within issues addressed by the SDAC and the instructor and staff are not informed about this in advance, this prevents us from helping during the semester, and it is unfair to request special considerations at the end of the term or after work is completed. So we request you inform the instructor as early in the term as possible your circumstances. If you have other special circumstances (athletics, other university-related activities, etc.) please contact your instructor and/or TA as soon as you know these may affect you in class.
