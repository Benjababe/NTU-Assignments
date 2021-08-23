class Q2 {

    public static void main(String[] args) {

    }
}

class School {
    String name;
    String[] courseCodes;
    Lecturer[] lecturers;
    Tutor[] tutors;
    Room[] rooms;
    int studentCount;
}

class Teacher {
    String name, ID, phoneNo;
}

class Lecturer extends Teacher {
    String[] lectureCodes;
}

class Tutor extends Teacher {
    String[] tutorialCodes;
}

class Student {
    String name, ID, email;
}

class Room {
    String roomNo;
    int occupancy;
    int[] size, classes;
}