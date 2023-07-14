# KRL Parser

I started this project to educate myself about industrial robot kinematics and code interpretation. I've been working on
virtual commissioning for automotive sector on KUKA robots and existing virtual code interpreters were terribly slow, so 
I found that there is probably area for improvement.

### Short details

- Program is able to execute KRL script with robot cartesian motion and prints robot axes values, inverse kinematics is used,
- Inverse kinematic solver is tested with a lot of test cases (30+), for every configuration of KUKA robot arm,
- ANTLR Grammar for KUKA KRL language is used, from official repo, but modified,
- Basic interpretation works, based on nice explanation of interpretation process from [Ruslan's Spivak blog](https://ruslanspivak.com/),
- It's really BASIC interpretation; global variables, nested calls etc. will not work.

### License

[MIT](https://choosealicense.com/licenses/mit/) ?