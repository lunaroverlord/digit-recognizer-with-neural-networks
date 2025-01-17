#!/usr/bin/python

"""The script trains a custom 256-25-10 neural network using train-digits.arff training set and
   tests it on test-digits.arff examples. It achieves 90% accuracy.
   Then it plots probabilities for a random digit from testing set as well as
   overall percent of correct guesses.
   Datasets that I used can be downloaded from
   http://www.seewald.at/en/2009/04/handwritten_digit_recognition"""

__author__ = "Ingvaras Merkys"

from ffnet import ffnet, mlgraph, readdata
import numpy as np
import scipy.io, scipy.io.arff, scipy.misc

def downscale(values):
   """Downscale an image, returns vector with 64 values"""
   return (scipy.misc.imresize(values.reshape(16,16), (8,8))).reshape(64)
   
def get_vector(x):
   """Takes label (int) and produces target vector"""
   a = [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ]
   a[int(x)] = 1
   return a

def get_digits_labels(filename):
    """Loads arff files"""
    data = scipy.io.arff.loadarff(filename)[0]
    N = len(data)
    D = len(data[0]) - 1
    digits = np.zeros((N, D))
    labels = np.zeros(N)
    for (nn,record) in enumerate(data):
        digits[nn,:] = np.array(list(record)[:-1])
        labels[nn] = int(list(record)[-1])
    return digits, labels
#    return map(downscale, digits), labels


print "LOADING DATA..."

input_values, train_labels = get_digits_labels('train-digits.arff')
target = map(get_vector, train_labels)

test_values, test_labels = get_digits_labels('test-digits.arff')
test_target = map(get_vector, test_labels)

# This custom network is explained in "hidden layer.pdf"
conec = [(1, 257), (2, 257), (3, 257), (4, 257), (5, 258), (6, 258), (7, 258), (8, 258), (9, 259), (10, 259), (11, 259),
(12, 259), (13, 260), (14, 260), (15, 260), (16, 260), (17, 257), (18, 257), (19, 257), (20, 257), (21, 258), (22, 258),
(23, 258), (24, 258), (25, 259), (26, 259), (27, 259), (28, 259), (29, 260), (30, 260), (31, 260), (32, 260), (33, 257),
(34, 257), (35, 257), (36, 257), (37, 258), (38, 258), (39, 258), (40, 258), (41, 259), (42, 259), (43, 259), (44, 259),
(45, 260), (46, 260), (47, 260), (48, 260), (49, 257), (50, 257), (51, 257), (52, 257), (53, 258), (54, 258), (55, 258),
(56, 258), (57, 259), (58, 259), (59, 259), (60, 259), (61, 260), (62, 260), (63, 260), (64, 260), (65, 261), (66, 261),
(67, 261), (68, 261), (69, 262), (70, 262), (71, 262), (72, 262), (73, 263), (74, 263), (75, 263), (76, 263), (77, 264),
(78, 264), (79, 264), (80, 264), (81, 261), (82, 261), (83, 261), (84, 261), (85, 262), (86, 262), (87, 262), (88, 262),
(89, 263), (90, 263), (91, 263), (92, 263), (93, 264), (94, 264), (95, 264), (96, 264), (97, 261), (98, 261), (99, 261),
(100, 261), (101, 262), (102, 262), (103, 262), (104, 262), (105, 263), (106, 263), (107, 263), (108, 263), (109, 264),
(110, 264), (111, 264), (112, 264), (113, 261), (114, 261), (115, 261), (116, 261), (117, 262), (118, 262), (119, 262),
(120, 262), (121, 263), (122, 263), (123, 263), (124, 263), (125, 264), (126, 264), (127, 264), (128, 264), (129, 265),
(130, 265), (131, 265), (132, 265), (133, 266), (134, 266), (135, 266), (136, 266), (137, 267), (138, 267), (139, 267),
(140, 267), (141, 268), (142, 268), (143, 268), (144, 268), (145, 265), (146, 265), (147, 265), (148, 265), (149, 266),
(150, 266), (151, 266), (152, 266), (153, 267), (154, 267), (155, 267), (156, 267), (157, 268), (158, 268), (159, 268),
(160, 268), (161, 265), (162, 265), (163, 265), (164, 265), (165, 266), (166, 266), (167, 266), (168, 266), (169, 267),
(170, 267), (171, 267), (172, 267), (173, 268), (174, 268), (175, 268), (176, 268), (177, 265), (178, 265), (179, 265),
(180, 265), (181, 266), (182, 266), (183, 266), (184, 266), (185, 267), (186, 267), (187, 267), (188, 267), (189, 268),
(190, 268), (191, 268), (192, 268), (193, 269), (194, 269), (195, 269), (196, 269), (197, 270), (198, 270), (199, 270),
(200, 270), (201, 271), (202, 271), (203, 271), (204, 271), (205, 272), (206, 272), (207, 272), (208, 272), (209, 269),
(210, 269), (211, 269), (212, 269), (213, 270), (214, 270), (215, 270), (216, 270), (217, 271), (218, 271), (219, 271),
(220, 271), (221, 272), (222, 272), (223, 272), (224, 272), (225, 269), (226, 269), (227, 269), (228, 269), (229, 270),
(230, 270), (231, 270), (232, 270), (233, 271), (234, 271), (235, 271), (236, 271), (237, 272), (238, 272), (239, 272),
(240, 272), (241, 269), (242, 269), (243, 269), (244, 269), (245, 270), (246, 270), (247, 270), (248, 270), (249, 271),
(250, 271), (251, 271), (252, 271), (253, 272), (254, 272), (255, 272), (256, 272), (35, 273), (36, 273), (37, 273),
(38, 274), (39, 274), (40, 274), (41, 275), (42, 275), (43, 275), (44, 276), (45, 276), (46, 276), (51, 273), (52, 273),
(53, 273), (54, 274), (55, 274), (56, 274), (57, 275), (58, 275), (59, 275), (60, 276), (61, 276), (62, 276), (67, 273),
(68, 273), (69, 273), (70, 274), (71, 274), (72, 274), (73, 275), (74, 275), (75, 275), (76, 276), (77, 276), (78, 276),
(83, 273), (84, 273), (85, 273), (86, 274), (87, 274), (88, 274), (89, 275), (90, 275), (91, 275), (92, 276), (93, 276),
(94, 276), (99, 276), (100, 276), (101, 276), (102, 277), (103, 277), (104, 277), (105, 278), (106, 278), (107, 278),
(108, 279), (109, 279), (110, 279), (115, 276), (116, 276), (117, 276), (118, 277), (119, 277), (120, 277), (121, 278),
(122, 278), (123, 278), (124, 279), (125, 279), (126, 279), (121, 276), (122, 276), (123, 276), (124, 277), (125, 277),
(126, 277), (127, 278), (128, 278), (129, 278), (130, 279), (131, 279), (132, 279), (133, 280), (134, 280), (135, 280),
(136, 281), (137, 281), (138, 281), (139, 282), (140, 282), (141, 282), (142, 283), (147, 276), (148, 276), (149, 276),
(150, 277), (151, 277), (152, 277), (153, 278), (154, 278), (155, 278), (156, 279), (157, 279), (158, 279), (163, 279),
(164, 279), (165, 279), (166, 280), (167, 280), (168, 280), (169, 281), (170, 281), (171, 281), (172, 282), (173, 282),
(174, 282), (179, 279), (180, 279), (181, 279), (182, 280), (183, 280), (184, 280), (185, 281), (186, 281), (187, 281),
(188, 282), (189, 282), (190, 282), (195, 279), (196, 279), (197, 279), (198, 280), (199, 280), (200, 280), (201, 281),
(202, 281), (203, 281), (204, 282), (205, 282), (206, 282), (211, 279), (212, 279), (213, 279), (214, 280), (215, 280),
(216, 280), (217, 281), (218, 281), (219, 281), (220, 282), (221, 282), (222, 282), (257, 282), (257, 283), (257, 284),
(257, 285), (257, 286), (257, 287), (257, 288), (257, 289), (257, 290), (257, 291), (258, 282), (258, 283), (258, 284),
(258, 285), (258, 286), (258, 287), (258, 288), (258, 289), (258, 290), (258, 291), (259, 282), (259, 283), (259, 284),
(259, 285), (259, 286), (259, 287), (259, 288), (259, 289), (259, 290), (259, 291), (260, 282), (260, 283), (260, 284),
(260, 285), (260, 286), (260, 287), (260, 288), (260, 289), (260, 290), (260, 291), (261, 282), (261, 283), (261, 284),
(261, 285), (261, 286), (261, 287), (261, 288), (261, 289), (261, 290), (261, 291), (262, 282), (262, 283), (262, 284),
(262, 285), (262, 286), (262, 287), (262, 288), (262, 289), (262, 290), (262, 291), (263, 282), (263, 283), (263, 284),
(263, 285), (263, 286), (263, 287), (263, 288), (263, 289), (263, 290), (263, 291), (264, 282), (264, 283), (264, 284),
(264, 285), (264, 286), (264, 287), (264, 288), (264, 289), (264, 290), (264, 291), (265, 282), (265, 283), (265, 284),
(265, 285), (265, 286), (265, 287), (265, 288), (265, 289), (265, 290), (265, 291), (266, 282), (266, 283), (266, 284),
(266, 285), (266, 286), (266, 287), (266, 288), (266, 289), (266, 290), (266, 291), (267, 282), (267, 283), (267, 284),
(267, 285), (267, 286), (267, 287), (267, 288), (267, 289), (267, 290), (267, 291), (268, 282), (268, 283), (268, 284),
(268, 285), (268, 286), (268, 287), (268, 288), (268, 289), (268, 290), (268, 291), (269, 282), (269, 283), (269, 284),
(269, 285), (269, 286), (269, 287), (269, 288), (269, 289), (269, 290), (269, 291), (270, 282), (270, 283), (270, 284),
(270, 285), (270, 286), (270, 287), (270, 288), (270, 289), (270, 290), (270, 291), (271, 282), (271, 283), (271, 284),
(271, 285), (271, 286), (271, 287), (271, 288), (271, 289), (271, 290), (271, 291), (272, 282), (272, 283), (272, 284),
(272, 285), (272, 286), (272, 287), (272, 288), (272, 289), (272, 290), (272, 291), (273, 282), (273, 283), (273, 284),
(273, 285), (273, 286), (273, 287), (273, 288), (273, 289), (273, 290), (273, 291), (274, 282), (274, 283), (274, 284),
(274, 285), (274, 286), (274, 287), (274, 288), (274, 289), (274, 290), (274, 291), (275, 282), (275, 283), (275, 284),
(275, 285), (275, 286), (275, 287), (275, 288), (275, 289), (275, 290), (275, 291), (276, 282), (276, 283), (276, 284),
(276, 285), (276, 286), (276, 287), (276, 288), (276, 289), (276, 290), (276, 291), (277, 282), (277, 283), (277, 284),
(277, 285), (277, 286), (277, 287), (277, 288), (277, 289), (277, 290), (277, 291), (278, 282), (278, 283), (278, 284),
(278, 285), (278, 286), (278, 287), (278, 288), (278, 289), (278, 290), (278, 291), (279, 282), (279, 283), (279, 284),
(279, 285), (279, 286), (279, 287), (279, 288), (279, 289), (279, 290), (279, 291), (280, 282), (280, 283), (280, 284),
(280, 285), (280, 286), (280, 287), (280, 288), (280, 289), (280, 290), (280, 291), (281, 282), (281, 283), (281, 284),
(281, 285), (281, 286), (281, 287), (281, 288), (281, 289), (281, 290), (281, 291)]
net = ffnet(conec)

print "TRAINING NETWORK..."
net.train_tnc(input_values[:1000], target[:1000], maxfun = 1000, messages = 1)

print "TESTING NETWORK..."
output, regression = net.test(test_values, test_target, iprint = 1)

correct = 0
incorrect = 0
for i in range(len(output)):
   if np.argmax(output[i]) == test_labels[i]:
      correct += 1
   else:
      incorrect += 1
accuracy = (correct/(correct + incorrect + 0.0))*100

print "Correct:", correct, "; Incorrect:", incorrect
print "Accuracy:", accuracy, "%"

# Show plot
try:
    from pylab import *
    from random import randint

    digitpat = randint(1, 1796) # Choosing random image to plot

    subplot(211)
    imshow(input_values[digitpat].reshape(16,16), interpolation = 'nearest')

    subplot(212)
    N = 10            # number of digits / network outputs
    ind = arange(N)   # the x locations for the groups
    width = 0.35      # the width of the bars
    bar(ind, net(input_values[digitpat]), width, color='b') #make a plot
    xticks(ind+width/2., ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'))
    xlim(-width,N-width)
    axhline(linewidth=1, color='black')
    title("Trained network (256-25-10) guesses a digit above...")
    xlabel("Digit")
    ylabel("Network outputs")

    subplot(212)
    title('Accuracy:' + str(accuracy) + '%')
    show()
except ImportError, e:
    print "Cannot make plots. For plotting install matplotlib.\n%s" % e
