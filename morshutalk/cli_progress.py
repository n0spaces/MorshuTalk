from tqdm import tqdm


class CliProgress:
    def __init__(self):
        self.pbar: tqdm | None = None

    def update_progress(self, major_step, minor_step, minor_total):
        if minor_step == 0:
            if self.pbar:
                self.pbar.close()
            desc = ""
            if major_step == 0:
                desc = "Reading text (step 1 of 2)"
            elif major_step == 1:
                desc = "Stitching audio (step 2 of 2)"
            self.pbar = tqdm(desc=desc, total=minor_total, leave=False)

        else:
            self.pbar.update(1)
            if minor_step == minor_total:
                self.pbar.close()
                self.pbar.refresh()
