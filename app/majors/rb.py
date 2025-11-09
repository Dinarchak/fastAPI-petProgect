class RBMajors:
    def __init__(self,
                 major_name: str | None = None,
                 major_description: str | None = None,
                 count_students: int | None = None
                ):
        self.major_name = major_name
        self.major_description = major_description
        self.count_students = count_students

    def to_dict(self):
        data = {
            'major_name': self.major_name,
            'major_description': self.major_description,
            'count_students': self.count_students
        }

        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data
