from fastapi import HTTPException, status


class NoDataException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                'status': status.HTTP_404_NOT_FOUND,
                'msg': "No data available for the given coordinates",
                'result': "Some error message"
            }
        )
        
class AvgException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HT,
            detail={
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'msg': "Average calculation went wrong. Please try again later.",
                'result': "Some error message"
            }
        )
