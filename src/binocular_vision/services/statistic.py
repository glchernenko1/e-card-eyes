from fastapi import HTTPException, status

from binocular_vision.models.progress_patient import ProgressPatientOneIteration, ProgressPatientBase


class Statistics:

    @staticmethod
    def statistic_two_end(list_progress_iteration: list[ProgressPatientOneIteration]) -> list[ProgressPatientBase]:
        """

        :param list_progress_iteration: должно быть больше двух
        :return:
        """

        execute = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Нехватает данных')
        if len(list_progress_iteration) < 2:
            raise execute
        list_last_progress = list_progress_iteration[0].progress
        list_pre_last_progress = list_progress_iteration[1].progress

        if list_last_progress is None or list_pre_last_progress is None:
            raise execute

        out = []
        for last_progress in list_last_progress:
            for pre_last_progress in list_pre_last_progress:
                if last_progress.progress_type == pre_last_progress.progress_type:
                    out.append(ProgressPatientBase(
                        progress_type=last_progress.progress_type,
                        progress_value=last_progress.progress_value - pre_last_progress.progress_value))
        return out
